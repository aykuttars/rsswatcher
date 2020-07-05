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

class RssPosts(Document):
    header       = StringField()
    detail       = StringField(null=True)
    url          = StringField()
    date         = DateTimeField(default=datetime.datetime.utcnow())
    provider     = StringField()
    image        = StringField()
    rank         = FloatField(max_length=3, choices=RANKS,default=0)
    users        = ListField()
class ExpiredJwtTokens(Document):
    token        = StringField(null=False)
    expired_date = DateTimeField()