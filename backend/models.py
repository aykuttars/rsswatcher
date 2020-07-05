from mongoengine import *
import datetime

RANKS = (0, 0.5, 1, 1.5, 2, 2.5 ,3,3.5,4,4.5,5)
class Users(Document):
    name         = StringField()
    surname      = StringField()
    username     = StringField(unique=True)
    passwd       = StringField()
    public_id    = StringField(unique=True)
    is_admin     = BooleanField(default=False)

class RssFeeds(Document):
    name         = StringField()
    url          = StringField()

class RssPosts(Document):
    header       = StringField(null=True)
    detail       = StringField(null=True)
    url          = StringField(null=True)
    date         = DateTimeField(default=datetime.datetime.utcnow(),null=True)
    provider     = StringField(null=True)
    image        = StringField(null=True)
    rank         = FloatField(max_length=3, choices=RANKS,default=0)
    users        = ListField(null=True)
class ExpiredJwtTokens(Document):
    token        = StringField(null=False)
    expired_date = DateTimeField()