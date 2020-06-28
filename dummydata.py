from mongoengine import connect
from dbschema import PatientStore, PatientMed, MedicineMaster
connect('hospital_database')

#MedicineMaster(med_id='PH1100',med_name='Pudin Hara',med_qty=50,med_rate=105).save()

ps = PatientStore.objects(ws_pat_id= 'SR7654321').first()
#mm = MedicineMaster.objects(med_id= 'P1250').first()
#PatientMed(pat_id= ps, med_id = mm, med_qty_issued= 5).save()
#MedicineMaster.objects(med_id= 'P1250').update_one(dec__med_qty= 5)

pm= PatientMed.objects.(pat_id=ps).first()

print(pm.pat_id.ws_pat_name)
