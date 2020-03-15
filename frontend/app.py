from flask import Flask, render_template, flash, redirect, request, session, abort, make_response
import os
import requests
import json
app = Flask(__name__)

@app.route('/')
def home():
    print("token",request.cookies.get('token'))
    if not request.cookies.get('token'):
        return render_template('login.html')
    else:
        return render_template('home.html')


@app.route('/logout/')
def logout():
    print("token",request.cookies.get('token'))
    resp = make_response(redirect('/'))
    resp.set_cookie('token', expires=0)
    return resp


@app.route('/login/', methods=['POST'])
def do_admin_login():
    backend_response = requests.post("http://127.0.0.1:8000/user/login",
                                     data={"username":request.form['username'],"password":request.form['password']})
    response = json.loads(backend_response.json())
    data = json.loads(response['data'])
    if response['status'] == 200:
        #session['logged_in'] = True
        #print(data['username'])
        resp = make_response(redirect('/'))
        resp.set_cookie('token',data['token'])
        return resp
    else:
        flash('Invalid Credentials')
        resp = make_response(redirect('/'))
        return resp

if __name__ == "__main__":
   app.secret_key = os.urandom(12)
   app.run(debug=True, host="0.0.0.0")

'''
Note to Moore/Frontend Dev

-Store token for logged users (check flask or implement own)
    -Done by using cookies
Review Response from backend (JSON/Dictionary)
    status = status of the query (200 = ok, 404 = not found, etc)
    data = JSON/Dictionary of other details that will return
'''