import base64
import requests
import json

public_key = 'pk-Z0OSzLvIcOI2UIvDhdTGVVfRSSeiGStnceqwUE7n0Ah'
secret_key = 'X8qolYjy62kIzEbr0QRK1h4b4KDVHaNcwMYk39jInSl'


def getAuthToken():
    token = base64.b64encode((public_key + ':' + secret_key).encode("utf-8"))
    return token.decode()

def getPublicAuthToken():
    token = base64.b64encode((public_key + ':').encode("utf-8"))
    return token.decode()

def getSecretAuthToken():
    token = base64.b64encode((':' + secret_key).encode("utf-8"))
    return token.decode()


def createTransaction(payload):

    headers = {'Authorization': 'Basic ' + getPublicAuthToken(), 'content-type': 'application/json'}
    response = requests.request('POST',  'https://pg-sandbox.paymaya.com/checkout/v1/checkouts', headers=headers,
                                data=json.dumps(payload))
    return json.loads(response.text.encode('utf8'))
