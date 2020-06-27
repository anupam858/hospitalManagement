from flask import Flask, render_template,redirect, request, Blueprint, flash,session, url_for

bp = Blueprint('hospitalmanagement' ,__name__)

@bp.route('/')
def home():
    if 'username' and 'password' in session.keys():
        return render_template('registration.html')
    return render_template("login.html")

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            flash('Wrong Credentials', 'error')
            return redirect(url_for('home'))
    
        else:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
    return render_template("registration.html")

@bp.route('/logout')
def logout():
    session.pop('username')
    session.pop('password')
    return redirect(url_for(home))
            
        
        
          
