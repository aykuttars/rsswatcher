from flask import Flask, request, jsonify, make_response
from mongoengine import *
from mongoengine.queryset.visitor import Q as QM
from PIL import Image
from werkzeug.security import generate_password_hash as makepasswd, check_password_hash as chkpasswd
from functools import wraps
from collections import OrderedDict
from bs4 import BeautifulSoup
from flask_apscheduler import APScheduler
from models import Users, RssFeeds, RssPosts, ExpiredJwtTokens
from flask_cors import CORS
import traceback
import json
import xmltodict
import requests
import datetime
import pytz
import jwt
import uuid
import dateparser

myapp = Flask(__name__)
CORS(myapp)
scheduler = APScheduler()
myapp.config['SECRET_KEY'] ='y0gve&v@x8efft-+gycp(pm!l8koa_+d4uecr&bm*l49%!'
myapp.config['JSON_AS_ASCII'] = False
connect('rsswatch',host='127.0.0.1', username='example', password='example', authentication_source='admin')
myapp.config['MONGODB_CONNECT'] = True

####################--JWT-Decorator--###################
def token_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        token =None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            is_expires = ExpiredJwtTokens.objects.filter(token=token).first()
            if is_expires:
                return jsonify({'message':'Token is invalid!'}),401
        if not token:
            return jsonify({'message':'Token is required!'}),401
        try:
            jwt_token = jwt.decode(token,myapp.config['SECRET_KEY'])
            if 'expires' in jwt_token:
                date_time_obj = datetime.datetime.strptime(jwt_token['expires'], '%Y-%m-%d %H:%M:%S.%f')
                now =datetime.datetime.utcnow()-datetime.timedelta(minutes =30)
                if date_time_obj<now:
                    return jsonify({'message':'Token is invalid!'}),401
            user = Users.objects.filter(public_id= jwt_token['id']).first()
        except Exception as e:
            return jsonify({'message':'Token is invalid!','details':traceback.format_exc()}),401
        return f(user,*args,**kwargs)
    return decorator
###################--Rss-Parse--########################
def rss_parser():
    rss_list = RssFeeds.objects.all()
    for rss in rss_list:
        response = requests.get(rss.url)
        response.encoding = response.apparent_encoding
        encoding = response.encoding if "charset" in response.headers.get("content-type", "").lower() else "ISO-8859"
        resp_text = json.loads(json.dumps(xmltodict.parse(response.text)))
        header   = "empty"
        detail   = "empty"
        url      = "empty"
        date     = "empty"
        provider = "empty"
        users = [ user.public_id for user in Users.objects.all()]
        if 'rss'in resp_text and 'channel' in resp_text['rss'] and 'item' in resp_text['rss']['channel']:
            for items in resp_text['rss']['channel']['item']:
                header = items['title']
                url    = items['link']
                date   = dateparser.parse(items['pubDate'])
                if not bool(BeautifulSoup(items['description'], "html.parser").find()):
                    detail=items['description']
                else:
                    parsed_html = BeautifulSoup(items['description'],"html.parser")
                    tags = ['img','a','br']
                    for tag in tags:
                        elements = parsed_html.find_all(tag)
                        for element in elements:
                            element.decompose()
                    detail = parsed_html.decode('utf8')
                if 'ipimage' in items:
                    image = items['ipimage']
                elif 'enclosure'  in items:
                    image = items['enclosure']['@url']
                elif 'image' in items:
                    image = items['image']
                rsspost = RssPosts()
                rsspost.header=header
                rsspost.detail=detail
                rsspost.image =image
                rsspost.url=url
                rsspost.date=date
                rsspost.provider = rss.name
                rsspost.users =users
                check =RssPosts.objects.filter(url =url).first()
                if not check:
                    rsspost.save()
        if 'feed'in resp_text and 'entry' in resp_text['feed']:
            for items in resp_text['feed']['entry']:
                if items['title']['@type'] =='text':
                    header = items['title']['#text']
                if items['link']['@rel'] =='alternate':
                    url    =  items['link']['@href']
                if items['summary']['@type'] =='text':
                    if not bool(BeautifulSoup(items['summary']['#text'], "html.parser").find()):
                        detail=items['summary']['#text']
                date   = dateparser.parse(items['published'])
                if items['content']['@type']=='html':
                    image = items['content']['#text']
                rsspost = RssPosts()
                rsspost.header=header
                rsspost.detail=detail
                rsspost.image =image
                rsspost.url=url
                rsspost.date=date
                rsspost.provider = rss.name
                rsspost.users =users
                check =RssPosts.objects.filter(url =url).first()
                if not check:
                    rsspost.save()
    count =RssPosts.objects.all().count()
def delete_old_tokens():
    tokens = ExpiredJwtTokens.objects.filter(expired_date__lte=datetime.datetime.utcnow())
    tokens.delete()
###################--User-Operations--##################
@myapp.route('/users',methods=['GET'])
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
@myapp.route('/users/<public_id>',methods=['GET'])
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

@myapp.route('/users',methods=['POST'])
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
@myapp.route('/users/<public_id>',methods=['PUT'])
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
@myapp.route('/users/<public_id>',methods=['DELETE'])
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
@myapp.route('/login',methods=['POST','DELETE'])
def login():
    if request.method == 'DELETE':
        if  request.headers.get('x-access-token'):
            token =request.headers.get('x-access-token')
            jwt_token = jwt.decode(token,myapp.config['SECRET_KEY'])
            if jwt_token.get('expires'):
                deleted_token =ExpiredJwtTokens.objects.create(
                    token =token,
                    expired_date=jwt_token.get('expires')
                )
                if(deleted_token.pk):
                    return jsonify({'message':'Successfully logged out'})
                
    authentication = request.get_json()
    if not authentication or not authentication['username'] or not authentication['password']:
        return make_response({'message':'Username or password wrong','status':'error'},404)
    user = Users.objects.filter(username=authentication['username']).first()

    if not user:
        return make_response({'message':'Username or password wrong','status':'error'},401)

    if chkpasswd(user.passwd,authentication['password']):
        token     = jwt.encode({'id':user.public_id,'expires':str(datetime.datetime.utcnow()+datetime.timedelta(minutes =30))},myapp.config['SECRET_KEY'],algorithm='HS256')
        resp_body = {'user_name':user.username,'token_expires':pytz.utc.localize(datetime.datetime.utcnow()+datetime.timedelta(minutes =30)).isoformat(),'jwt_token':token.decode('UTF-8'),'is_admin':user.is_admin}
        resp      = jsonify(resp_body)
        resp.headers['Access-Control-Token'] = token.decode('UTF-8')
        return resp
    return make_response({'message':'Username or password wrong','status':'error'},401)
##################################-- RSS---- LIST--############################
@myapp.route('/feeds',methods=['GET'])
@token_required
def search_feeds(current_user):
    start  = 0
    length = 10
    date   = None
    if request.args.get('start'):
        start=request.args.get('start')
    if request.args.get('length'):
        length = request.args.get('length')
    if not isinstance(request.args.get('time'),datetime.date):
        date =request.args.get('time')
    elif isinstance(request.args.get('time'),datetime.date):
        date = datetime.datetime.strptime(request.args.get('time'), '%Y-%m-%d %H:%M:%S')
        
    search =  request.args.get('search')
    
    if request.args.get('draw'):
        if request.args.get('search[value]'):
            search = request.args.get('search[value]')
        
    rss_objects = RssPosts.objects.all()
    total_count = rss_objects.count()
    if search:
        rss_objects=rss_objects.filter(QM(header__icontains =search)|
                                       QM(detail__icontains = search)|
                                       QM(provider__icontains=search))
    if date:
        if isinstance(date,datetime.date):
            search_date = date
        elif  '_' in date and date.split('_')[1] =='day':
            search_date = datetime.datetime.utcnow()-datetime.timedelta(days =int(date.split('_')[0]))
        elif '_' in date and date.split('_')[1] =='hour':
            search_date = datetime.datetime.utcnow()-datetime.timedelta(hours =int(date.split('_')[0]))
        if isinstance(search_date,datetime.date):
            rss_objects = rss_objects.filter(date__gte = search_date)
    
    rss_objects = rss_objects.skip(int(start)).limit(int(length)).order_by('date')
    
    rss_list = []
    for rss in rss_objects:
        rss_dict = {}
        rss_dict['id'] = str(rss.pk)
        rss_dict['header'] = rss.header
        rss_dict['detail'] = rss.detail
        rss_dict['url'] = rss.url
        rss_dict['date'] = pytz.utc.localize(rss.date).isoformat()
        rss_dict['provider'] = rss.provider
        rss_dict['image'] = rss.image
        rss_dict['rank'] = rss.rank
        rss_list.append(rss_dict)
    filtered_count = rss_objects.count()
    if request.args.get('draw'):
        return jsonify({"draw":request.args.get('draw'),"data":rss_list,"recordsFiltered":filtered_count,"recordsTotal":total_count})
    return jsonify({"data":rss_list,"recordsFiltered":filtered_count,"recordsTotal":total_count})


@myapp.route('/feeds/<id>',methods=['PUT'])
@token_required
def update_feeds(current_user, id):
    data = request.get_json().get('rank')
    if isinstance(data, float) or isinstance(data, int):
        feed = RssPosts.objects.filter(pk = id).first()
        if data <0:
            data =0
        elif data >5:
            data = 5
        feed.rank = data
        feed.save()
        return jsonify({"status": "success"})
    return make_response({'message':'Wrong rank value','status':'error'},400)
scheduler.add_job(id="jwt expires checker",func=delete_old_tokens,trigger='interval',minutes =2)
scheduler.add_job(id="Rss Pusher",func=rss_parser,trigger='interval',minutes =15)
scheduler.start()
if __name__ == '__main__':
    myapp.run(debug =True)
