import mongoengine as me

class UserStore(me.Document):

    user_id = me.StringField(required=True)
    password = me.StringField(required=True)
    time_stamp = me.DateTimeField()
