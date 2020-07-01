from flask import Flask,request,jsonify
from mongoengine import *
from PIL import Image

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
app.config['MONGODB_CONNECT'] = True

if __name__ == '__main__':

    app.run(debug =True)