from flask import Flask, render_template, flash, redirect, request, session, abort
import os
import requests
import json
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/Login', methods=['POST'])
def do_admin_login():
    backend_response = requests.post("http://127.0.0.1:8000/user/login",
                                     data={"username":request.form['username'],"password":request.form['password']})
    response = json.loads(backend_response.json())
    print(response['data'])
    if response['status'] == 200:
        #session['logged_in'] = True
        return render_template('home.html')
    else:
        flash('Invalid Credentials')
        return home()

if __name__ == "__main__":
   app.secret_key = os.urandom(12)
   app.run(debug=True, host="0.0.0.0")

'''
Note to Moore/Frontend Dev

-Store token for logged users (check flask or implement own)
Review Response from backend (JSON/Dictionary)
    status = status of the query (200 = ok, 404 = not found, etc)
    data = JSON/Dictionary of other details that will return
'''
