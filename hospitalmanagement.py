from flask import Flask, render_template,redirect, request, Blueprint, flash,session, url_for
from .dbschema import UserStore, PatientStore
from datetime import datetime
from werkzeug.security import generate_password_hash

bp = Blueprint('hospitalmanagement' ,__name__)

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
def patient_reg():

    return(render_template("registration.html"))

@bp.route('/register', methods=['POST'])
def register():

    try:
        id = str(request.form.bed_type) + str(request.form.pat_ssn[2:9])
        pat= PatientStore(w_ssn= request.form.pat_ssn)
        pat.ws_pat_id = id
        pat.ws_pat_name = request.form.pat_name
        pat.ws_age = request.form.pat_age
        pat.ws_doj = request.form.pat_doa
        pat.ws_rtype = request.form.bed_type
        pat.ws_adrs = request.form.pat_address
        pat.ws_city = request.form.pat_city
        pat.ws_state = request.form.pat_state
        pat.ws_status = 1
        print(id, request.form.pat_doa)
        pat.save()
        flash("Patient Registered","message")
    except:
        flash("Registration Failed","error")


    return redirect(url_for("hospitalmanagement.patient_reg"), 404)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for(home))