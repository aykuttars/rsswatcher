from flask import Flask,request,jsonify,make_response
from mongoengine import *
from PIL import Image
from werkzeug.security import generate_password_hash as makepasswd,check_password_hash as chkpasswd
from functools import wraps
import datetime
import jwt
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] ='y0gve&v@x8efft-+gycp(pm!l8koa_+d4uecr&bm*l49%!'
connect('rsswatch',host='192.168.1.14', username='example', password='example', authentication_source='admin')
app.config['MONGODB_CONNECT'] = True

######################--MODELS--########################
RANKS = (0, 0.5, 1, 1.5, 2, 2.5 ,3,3.5,4,4.5,5)
class Users(Document):
    name         = StringField()
    surname      = StringField()
    username     = StringField(unique=True)
    passwd       = StringField()
    public_id    = StringField(unique=True)
    is_admin     = BooleanField(default=False)

class RssPosts(Document):
    header       = StringField()
    information  = StringField()
    detail       = StringField()
    url          = StringField()
    date         = DateTimeField(default=datetime.datetime.utcnow())
    provider     = StringField()
    image        = ImageField()
    rank         = StringField(max_length=3, choices=RANKS)
    users        = ListField()
####################--JWT-Decorator--###################
def token_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        token =None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is required!'}),401
        try:
            jwt_token = jwt.decode(token,app.config['SECRET_KEY'])
            if 'expires' in jwt_token:
                date_time_obj = datetime.datetime.strptime(jwt_token['expires'], '%Y-%m-%d %H:%M:%S.%f')
                diff =date_time_obj-datetime.datetime.utcnow()
                if int(str(diff).split(':')[1])<1:
                    return jsonify({'message':'Token is expired!'}),401
            user = Users.objects.filter(public_id= jwt_token['id']).first()
        except:
            return jsonify({'message':'Token is invalid!'}),401
        return f(user,*args,**kwargs)
    return decorator
###################--User-Operations--##################
@app.route('/users',methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.is_admin:
        return jsonify({'message':'you are not authorized user'})
    users = Users.objects.all()
    lst   = []
    for user in users:
        usr_dct= {}
        usr_dct['user_name'] = user.username
        usr_dct['name']      = user.name
        usr_dct['surname']   = user.surname
        usr_dct['id']        = user.public_id
        usr_dct['password']  = user.passwd
        usr_dct['is_admin']  = user.is_admin
        lst.append(usr_dct)

    return jsonify({'users':lst})
@app.route('/users/<public_id>',methods=['GET'])
@token_required
def get_one_user(current_user,public_id):
    if not current_user.is_admin:
        return jsonify({'message':'you are not authorized user'})
    user = Users.objects.filter(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    usr_dct= {}
    usr_dct['user_name'] = user.username
    usr_dct['name']      = user.name
    usr_dct['surname']   = user.surname
    usr_dct['id']        = user.public_id
    usr_dct['password']  = user.passwd

    return jsonify({'user':usr_dct})
    return ''
@app.route('/users',methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.is_admin:
        return jsonify({'message':'you are not authorized user'})
    data  =request.get_json()
    hashed_passwd = makepasswd(data['password'],method ='sha256')
    new_user = Users()
    new_user.name         = data['name']
    new_user.surname      = data['surname']
    new_user.username     = data['username']
    new_user.public_id    = str(uuid.uuid4())
    new_user.passwd       = hashed_passwd
    new_user.save()
    resp = {'Message':'New User Not Created'}
    if new_user:
        resp = {'Message':'New User Created'}
    return jsonify(resp)
@app.route('/users/<public_id>',methods=['PUT'])
@token_required
def update_user(current_user,public_id):
    if not current_user.is_admin:
        return jsonify({'message':'you are not authorized user'})
    user = Users.objects.filter(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    user.is_admin =True
    if user.save():
        return jsonify({'message':'The user has been authorized to admin'})
    else:
        return jsonify({'message':'The user has not been authorized to admin'})
@app.route('/users/<public_id>',methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):
    if not current_user.is_admin:
        return jsonify({'message':'you are not authorized user'})
    user = Users.objects.filter(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    user.delete()
    user = Users.objects.filter(public_id=public_id).first()
    if not user:
        return jsonify({'message':'The user has been deleted'})
    else:
        return jsonify({'message':'The user has not been deleted'})
@app.route('/login')
def login():
    authentication = request.authorization
    if not authentication or not authentication.username or not authentication.password:
        return make_response('Please check your login method',401,{'WWW-Authenticate':'Login required'})
    user = Users.objects.filter(username=authentication.username).first()

    if not user:
        return make_response('Please check your username',401,{'WWW-Authenticate':'Login required'})

    if chkpasswd(user.passwd,authentication.password):
        token = jwt.encode({'id':user.public_id,'expires':str(datetime.datetime.utcnow()+datetime.timedelta(minutes =30))},app.config['SECRET_KEY'],algorithm='HS256')
        print(token)
        return jsonify({'token':token.decode('UTF-8')})
    return make_response('Please check your password',401,{'WWW-Authenticate':'Login required'})
if __name__ == '__main__':

    app.run(debug =True)