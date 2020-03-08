from flask import Flask, render_template, flash, redirect, request, session, abort
import os

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/Login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin@gmail.com':
        session['logged_in'] = True
        return render_template('home.html')
    else:
        flash('wrong password!')
        return home()
	
if __name__ == "__main__":
   app.secret_key = os.urandom(12)
   app.run(debug=True, host="0.0.0.0")