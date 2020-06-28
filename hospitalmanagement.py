import functools
from flask import Flask, render_template,redirect, request, Blueprint, flash,session, url_for, abort, jsonify, json
from .dbschema import UserStore, PatientStore, PatientMed
from datetime import datetime
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

    if request.method=='GET':

        id = request.args.get('id')
        pat = PatientStore.objects(ws_pat_id=id)
        meds = PatientMed.objects(pat_id= pat)

        if pat_details== None and id is not None:
            flash('No Patient Found')

        return render_template('pharma.html', meds= meds)

    


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
            else:
                return abort(404)

    return abort(400)

@bp.route('/viewpatients', methods = ['GET'])
def view():
    if request.method == 'GET':
        pat = PatientStore.objects(ws_status= 1)
        if pat == None:
            flash('No active patients are available', "error")

        return render_template('viewpatients.html', patients=pat)

    return abort(400)

@bp.route('/update', methods=['POST','GET'])
def update():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Get_button':

            patient = PatientStore.objects(ws_pat_id= request.form['patient_id']).first()
            if patient==None:
                flash('Invalid Patient ID', "error")
                return render_template('update.html')
            else:
                patient = PatientStore.objects(ws_pat_id= request.form['patient_id']).first()
                return render_template('update.html', patient = patient)
            
        elif request.form['submit_button'] == 'Update_button':
            PatientStore.objects(ws_pat_id= request.form['patient_id']).update(patient_name = request.args.get('pat_name'),age = request.args.get('pat_age'),doj = request.args.get('pat_doa'),rtype = request.args.get('bed-type'),adrs = request.args.get('pat_address'),state = request.args.get('pat_state'),city = request.args.get('pat_city'))
            flash('Updated Successfully', "success")
            return render_template('update.html')

    else:
        return render_template("update.html")

@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for(home))