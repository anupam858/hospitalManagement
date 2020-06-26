import mongoengine as me

class UserStore(me.Document):

    user_id = me.StringField(required=True)
    password = me.StringField(required=True)
    time_stamp = me.DateTimeField()

class PatientStore(me.Document):

    ws_ssn = me.StringField(required=True)
    ws_pat_id = me.StringField()
    ws_pat_name = me.StringField(required=True)
    ws_age = me.IntField(required=True)
    ws_doj = me.DateTimeField(required=True)
    ws_rtype = me.StringField(required=True)
    ws_adrs = me.StringField(required=True)
    ws_city = me.StringField(required=True)
    ws_state = me.StringField(required=True)
    ws_status = me.IntField()

