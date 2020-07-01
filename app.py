from flask import Flask,request,jsonify
from mongoengine import *
from PIL import Image
from werkzeug.security import generate_password_hash as makepasswd,check_password_hash as chkpasswd
import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] ='y0gve&v@x8efft-+gycp(pm!l8koa_+d4uecr&bm*l49%!'
connect('rsswatch',host='192.168.1.14', username='example', password='example', authentication_source='admin')
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
@app.route('/users',methods=['GET'])
def get_all_users():
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
def get_one_user(public_id):
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
def create_user():
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
def update_user(public_id):
    user = Users.objects.filter(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    user.is_admin =True
    if user.save():
        return jsonify({'message':'The user has been authorized to admin'})
    else:
        return jsonify({'message':'The user has not been authorized to admin'})
@app.route('/users/<public_id>',methods=['DELETE'])
def delete_user(public_id):
    user = Users.objects.filter(public_id=public_id).first()
    if not user:
        return jsonify({'message':'No user found!'})
    user.delete()
    user = Users.objects.filter(public_id=public_id).first()
    if not user:
        return jsonify({'message':'The user has been deleted'})
    else:
        return jsonify({'message':'The user has not been deleted'})
app.config['MONGODB_CONNECT'] = True

if __name__ == '__main__':

    app.run(debug =True)