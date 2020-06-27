from flask import Flask, render_template,redirect, request, Blueprint, flash,session, url_for
from .dbschema import UserStore
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
        print(user)
        if user==None or user.get_password(request.form['password'])== False:
            flash('Wrong Credentials', "error")
            print(request.form['username'], request.form['password'], type(request.form['username']))
            return redirect(url_for('hospitalmanagement.home'))
    
        else:

            session['username'] = request.form['username']
            session['password'] = request.form['password']
            UserStore.objects(user_id= request.form['username']).update(time_stamp= datetime.now())
            return redirect(url_for('hospitalmanagement.patient_reg'))

@bp.route('/patientregistration', methods=['POST', 'GET'])
def patient_reg():
    return(render_template("registration.html"))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for(home))
            
        
        
          
