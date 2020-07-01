import functools
from flask import Flask, render_template,redirect, request, Blueprint, flash,session, url_for, abort, jsonify
from .dbschema import UserStore, PatientStore, PatientMed, MedicineMaster, PatientDiag
from datetime import datetime, date
from werkzeug.security import generate_password_hash

bp = Blueprint('hospitalmanagement' ,__name__)

def login_required(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if 'username' and 'password' in session.keys():
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('hospitalmanagement.home'))

    return wrap

@bp.route('/')
@bp.route('/home')
def home():
    if 'username' and 'password' in session.keys():
        return render_template('registration.html')
    return render_template("login.html")

@bp.route('/login', methods=['POST'])
def login():

    if request.method == 'POST':
        user = UserStore.objects(user_id= request.form['username']).first()
    
        if user==None or user.get_password(request.form['password'])== False:
            flash('Wrong Credentials', "error")
            print(request.form['username'], request.form['password'], type(request.form['username']))
            return redirect(url_for('hospitalmanagement.home'))
    
        else:

            session['username'] = request.form['username']
            session['password'] = request.form['password']
            UserStore.objects(user_id= request.form['username']).update(time_stamp= datetime.now())
            return redirect(url_for('hospitalmanagement.patient_reg'))

@bp.route('/patientregistration')
@login_required
def patient_reg():

    return(render_template("registration.html"))

@bp.route('/register', methods=['POST'])
@login_required
def register():


    id = str(request.form['bed_type']) + str(request.form['pat_ssn'][2:9])
    pat= PatientStore(ws_ssn= request.form['pat_ssn'])
    pat.ws_pat_id = str(id)
    pat.ws_pat_name = request.form['pat_name']
    pat.ws_age = request.form['pat_age']
    pat.ws_doj = datetime.strptime(request.form['pat_doa'], '%Y-%m-%dT%H:%M')
    pat.ws_rtype = request.form['bed_type']
    pat.ws_adrs = request.form['pat_address']
    pat.ws_city = request.form['pat_city']
    pat.ws_state = request.form['pat_state']
    pat.ws_status = 1
    print(id, request.form['pat_doa'])
    pat.save()
    flash("Patient Registered","message")
    


    return redirect(url_for("hospitalmanagement.patient_reg"))

@bp.route('/patientSearch')
@login_required
def pat_details():

    id = request.args.get('id')
    pat = PatientStore.objects(ws_pat_id= id).first()
    if pat==None and id is not None:
        flash('No Patient Found')
    
    return render_template('searchPatient.html', pat= pat)

@bp.route('/pharmacy/patientSearch', methods=['GET'])
@login_required
def pharm_pat_details():

    pat = None
    meds= None
    if request.method=='GET':

        id = request.args.get('id')

        if id != None:
            pat = PatientStore.objects(ws_pat_id=id).first()
            meds = PatientMed.objects(pat_id= pat)

        if pat== None and id is not None:
            flash('No Patient Found',"danger")
        

        return render_template('pharma.html', pat= pat, meds= meds)


@bp.route('/pharmacy/issuemeds', methods=['GET','POST'])
@login_required
def issueMedicine():
    
    if request.method== 'GET':
        return render_template('issue_med.html', pat= {'pat_id':request.args.get('issue_medicine')})

    if request.method== 'POST':

        req =request.get_json(force=True)
        if 'med_avail' in req.keys():

            med= MedicineMaster.objects(med_name= req["med_name"]).first()
            return jsonify(med)

        elif 'submit_button' in req.keys():
            pat_id = req["pat_id"]
            pat = PatientStore.objects(ws_pat_id= pat_id).first()

            for meds in req["data"]:
                mm = MedicineMaster.objects(med_id= meds['med_id']).first()
                PatientMed(pat_id= pat, med_id = mm, med_qty_issued= meds['qty_issued']).save()
                MedicineMaster.objects(med_id= meds['med_id']).update_one(dec__med_qty= meds['qty_issued'])

            return url_for('hospitalmanagement.pharm_pat_details', id= req["pat_id"])

    return abort(400)

@bp.route('/<string:section>/psearch', methods =['POST'])
@login_required
def search(section):

    if request.method == 'POST':

        id = request.form.get('pat_id')
        if id == None:
            return abort(400)

        else:

            if(section=='patientSearch'):
                return redirect(url_for('hospitalmanagement.pat_details', id = id))
            elif(section=='diagnosisPatSearch'):
                return redirect(url_for('hospitalmanagement.diag_pat_details', id = id))
            elif(section=='pharmacyPatSearch'):
                return redirect(url_for('hospitalmanagement.pharm_pat_details', id = id))
            elif(section=='billPatSearch'):
                return redirect(url_for('hospitalmanagement.bill_pat_details', id = id))
            else:
                return abort(404)

    return abort(400)

@bp.route('/viewpatients', methods = ['GET'])
@login_required
def view():
    if request.method == 'GET':
        pat = PatientStore.objects(ws_status= 1)
        if pat == None:
            flash('No active patients are available', "error")

        return render_template('viewpatients.html', patients=pat)

    return abort(400)

@bp.route('/update', methods=['POST','GET'])
@login_required
def update():
    patient=None
    if request.method == 'POST':
        if request.form['submit_button'] == 'Get_button':

            patient = PatientStore.objects(ws_pat_id= request.form['patient_id']).first()
            if patient==None:
                flash('Invalid Patient ID', "danger")
                return render_template('update.html', patient= patient)
            else:
                patient = PatientStore.objects(ws_pat_id= request.form['patient_id']).first()
                return render_template('update.html', patient = patient)
            
        elif request.form['submit_button'] == 'Update_button':

            try:

                PatientStore.objects(ws_pat_id= request.form['patient_id']).update(ws_pat_name = request.form['pat_name'],
                ws_age = request.form['pat_age'],ws_doj = datetime.strptime(request.form['pat_doa'], '%Y-%m-%dT%H:%M'),
                ws_rtype = request.form['bed_type'],ws_adrs = request.form['pat_address'],ws_state = request.form['pat_state'],
                ws_city = request.form['pat_city'])
                if PatientStore.objects(ws_pat_id= request.form['patient_id']).count()==1:
                    flash('Updated Successfully', "success")
                else:
                    raise Exception('Wrong Patient ID')
            except:
                flash('Update failed. Do not change Patient ID and ensure all the data is filled.', 'danger')
            return render_template('update.html', patient= patient)

    else:
        
        return render_template("update.html", patient= patient)

@bp.route('/delete', methods=['POST','GET'])
@login_required
def delete():

    patient= None
    if request.method == 'POST':
        
        if request.form['submit_button'] == 'Get_button':

            patient = PatientStore.objects(ws_pat_id= request.form['patient_id']).first()
            if patient==None:
                flash('Invalid Patient ID', "danger")
                return render_template('delete.html')
            else:
                patient = PatientStore.objects(ws_pat_id= request.form['patient_id']).first()
                return render_template('delete.html', patient = patient)

        elif request.form['submit_button'] == 'Delete_button':

            try:
                if PatientStore.objects(ws_pat_id= request.form['patient_id']).count()==1:
                    PatientStore.objects(ws_pat_id= request.form['patient_id']).delete()
                    flash('Deleted Successfully', "success")
                
                else:
                    raise Exception('Delete Exception')
            except:
                flash('Delete failed. Do not change Patient ID', 'danger')

            return render_template('delete.html', patient = patient)
        
    else:
        return render_template("delete.html", patient=patient)

@bp.route('/diagnostics/patientSearch', methods=['GET'])
@login_required
def diag_pat_details():

    pat = None
    tests= None
    if request.method=='GET':

        id = request.args.get('id')

        if id != None:
            pat = PatientStore.objects(ws_pat_id=id).first()
            tests = PatientDiag.objects(pat_id= pat)

        if pat== None and id is not None:
            flash('No Patient Found',"danger")
        

        return render_template('diagnostics.html', pat= pat, tests= tests)


@bp.route('/diagnosis/addtests', methods=['GET','POST'])
@login_required
def addDiag():
    
    if request.method== 'GET':
        tests = DiagnosticsMaster.objects();
        return render_template('add_diag.html', pat= {'pat_id':request.args.get('add_diag')}, tests = tests)

    if request.method== 'POST':

        req =request.get_json(force=True)
        if 'test_name' in req.keys():

            t= DiagnosticsMaster.objects(test_name= req["select_list"]).first()
            return jsonify(t)

        elif 'submit_button' in req.keys():
            pat_id = req["pat_id"]
            pat = PatientStore.objects(ws_pat_id= pat_id).first()

            for ts in req["data"]:
                dm = DiagnosticsMaster.objects(test_id= ts['test_id']).first()
                PatientDiag(pat_id= pat, test_id = dm).save()
                #DiagnosticsMaster.objects(test_id= ts['test_id']).update_one(dec__med_qty= meds['qty_issued'])

            return url_for('hospitalmanagement.diag_pat_details', id= req["pat_id"])

    return abort(400)
  
@bp.route('/bill', methods=['GET', 'POST'])
@login_required
def bill_pat_details():
    pat= None
    meds= None
    diag= None
    diff = None
    bill_room = 0
    bill_med = 0
    bill_diag = 0

    if request.method=="GET":
        id = request.args.get('id')
        
        if id is not None:
            pat = PatientStore.objects(ws_pat_id=id).first()
            diff = abs(datetime.now()-pat.ws_doj).days +1

            if(pat==None):
                flash("No Patient found for patient id","danger")

            else:
                meds = PatientMed.objects(pat_id= pat)
                diag= PatientDiag.objects(pat_id =pat)

                if pat.ws_rtype =='GW':
                    bill_room = 2000*diff
                elif pat.ws_rtype=='SS':
                    bill_room = 4000*diff
                else:
                    bill_room = 8000*diff
                
                for m in meds:
                    bill_med = bill_med + m.med_id.med_rate*m.med_qty_issued
                
                for d in diag:
                    bill_diag = bill_diag + d.test_id.test_charge

                if pat.ws_status==0:
                    flash("Patient Already Discharged","warning")

        return render_template('bill.html', pat= pat, meds= meds, diag= diag, diff=diff, bill_room = bill_room, bill_med=bill_med, bill_diag=bill_diag)

    if request.method=="POST":

        if request.form["discharge_button"]== request.args.get('id'):
            PatientStore.objects(pat_id=id).first().update_one(ws_status=0)
            flash("Patient Bill Generated","success")
            return redirect(url_for('bill_pat_details'))

    return abort(400)
    
@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('hospitalmanagement.home'))
