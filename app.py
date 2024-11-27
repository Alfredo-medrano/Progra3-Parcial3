from flask import Flask, render_template, redirect, url_for, session,jsonify
from login import login_bp
from Cenergia import cenergia_bp
from cAire import cAire_bp
from cClima import cclima_bp

app = Flask(__name__)
app.secret_key = '123456'

app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(cenergia_bp, url_prefix='/cenergia')
app.register_blueprint(cAire_bp, url_prefix='/cAire')
app.register_blueprint(cclima_bp, url_prefix='/cclima')


@app.route('/')
def home():
    if 'user_logged_in' not in session:
        return redirect(url_for('login.login'))
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user_logged_in' not in session:
        return redirect(url_for('login.login'))
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
