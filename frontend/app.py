from flask import Flask, render_template, flash, redirect, request, session, abort
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
        return render_template('home.html')
    else:
        flash('Invalid Credentials')
        return home()

if __name__ == "__main__":
   app.secret_key = os.urandom(12)
   app.run(debug=True, host="0.0.0.0")