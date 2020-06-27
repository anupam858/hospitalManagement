import mongoengine as me
from werkzeug.security import check_password_hash

class UserStore(me.Document):

    user_id = me.StringField(required=True)
    password = me.StringField(required=True)
    time_stamp = me.DateTimeField()

    def get_password(self, password):

        return check_password_hash(self.password, password)


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

class MedicineMaster(me.Document):

    med_id = me.StringField(required=True)
    med_name = me.StringField(required=True)
    med_qty = me.IntField(required=True)
    med_rate = me.FloatField(required=True)

class PatientMed(me.Document):

    pat_id = me.ReferenceField(PatientStore)
    med_id = me.StringField(required=True)
    med_qty_issued = me.IntField(required=True)

class DiagnosticsMaster(me.Document):

    test_id = me.StringField(required=True)
    test_name = me.StringField(required=True)
    test_charge = me.FloatField(required=True)

class PatientDiag(me.Document):

    pat_id = me.ReferenceField(PatientStore)
    test_id = me.StringField(required=True)

