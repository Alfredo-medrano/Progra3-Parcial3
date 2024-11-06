from flask import Blueprint, render_template, request, redirect, url_for, flash, session

login_bp = Blueprint('login', __name__)

USERNAME = 'admin'
PASSWORD = '12345'

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            session['user_logged_in'] = True  
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
    
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('user_logged_in', None)  
    return redirect(url_for('login.login'))
