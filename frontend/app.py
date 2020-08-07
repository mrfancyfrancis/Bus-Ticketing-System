from flask import Flask, render_template, flash, redirect, request, session, abort, make_response
import os
import requests
import json

app = Flask(__name__)

'''
This is to replace flask's 'static' as endpoint. In this case,
we replace 'static' as 'frontend' since all views of flask are 
migrated to frontend.
'''
# Set the static_url_path property.
a_new_static_path = '/frontend/static'
app.static_url_path = a_new_static_path

# Remove the old rule from Map._rules.
for rule in app.url_map.iter_rules('static'):
    app.url_map._rules.remove(rule)

# Remove the old rule from Map._rules_by_endpoint.
app.url_map._rules_by_endpoint['static'] = []  

# Add the updated rule.
app.add_url_rule(f'{a_new_static_path}/<path:filename>',
                 endpoint='frontend',
                 view_func=app.send_static_file)

@app.route('/')
def home():
    print("token",request.cookies.get('token'))
    if not request.cookies.get('token'):
        return render_template('login.html')
    else:
        info_response = requests.post("http://127.0.0.1:8000/user/info/",
                                            headers = {"Authorization": 'Token ' + request.cookies.get('token')}
                                            )
        reservation_response = requests.post("http://127.0.0.1:8000/user/reservations/",
                                            headers = {"Authorization": 'Token ' + request.cookies.get('token')}
                                            )
        info = json.loads(json.loads(info_response.json())['data'])
        reservations = json.loads(json.loads(reservation_response.json())['data'])['reservations']
        return render_template('home.html', info=info, reservations=reservations)

@app.route('/logout/')
def logout():
    print("token",request.cookies.get('token'))
    resp = make_response(redirect('/'))
    resp.set_cookie('token', expires=0)
    return resp


@app.route('/login/', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]


    backend_response = requests.post("http://127.0.0.1:8000/user/login",
                                     data = {"username": username,
                                             "password": password}
                                     )

    response = json.loads(backend_response.json())
    print(response)
    if response['status'] == 200:
        data = json.loads(response['data'])
        info = data['info']
        print(data, type(data))
        resp = make_response(redirect('/'))
        resp.set_cookie('token', data['token'])
        return resp
    else:
        flash('Invalid Credentials')
        resp = make_response(redirect('/'))
        return resp


@app.route('/book/')
def book():
    if not request.cookies.get('token'):
        resp = make_response(redirect('/'))
        return resp
    else:
        schedule_response = requests.post("http://127.0.0.1:8000/user/schedules/",
                                            headers = {"Authorization": 'Token ' + request.cookies.get('token')}
                                            )
        schedules = json.loads(schedule_response.json())['data']
        #schedules = json.loads(schedule_response.json())      
        print(schedules, type(schedules))  
    return render_template('book.html', schedules=schedules)

@app.route('/about/')
def about():
    if not request.cookies.get('token'):
        resp = make_response(redirect('/'))
        return resp
    else:
        return render_template('about.html')

@app.route('/buspartners/')
def buspartners():
    return render_template('buspartners.html')

@app.route('/payment/approved')
def approvepayment():
    id = request.args.get('id', type=int)
    if not request.cookies.get('token'):
        resp = make_response(redirect('/'))
        return resp
    else:
        print('payment id '+str(id))
        payment_response = requests.post("http://127.0.0.1:8000/user/payment/",
                                          headers={"Authorization": 'Token ' + request.cookies.get('token')},
                                          data={"payment_id": id}
                                          )
        payment = json.loads(payment_response.json())
        # schedules = json.loads(schedule_response.json())
        print(payment, type(payment))
    return render_template(payment)

if __name__ == "__main__":
   app.secret_key = os.urandom(12)
   app.run(debug=True, host="0.0.0.0")