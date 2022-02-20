from flask import Flask, request
from time import sleep 
import random
#from cryptography.fernet import Fernet

from base64 import urlsafe_b64encode, urlsafe_b64decode

import json

# Fernet
#fernet = Fernet("oYiV_ftSLe-YQjo9UqOWq0KGeiU1ovtCmBeV4XHaWew=")

app = Flask(__name__)

@app.route("/status")
def status():
    return "<p>I exist!</p>"

@app.route("/encrypt", methods=['PUT'])
def encrypt():
    data = json.loads(request.data)
    data_bin = data['data']
    print(f"len data: {len(data_bin)}")
    #print(data_bin)
    #sleep(random.randrange(10))
    #result = fernet.encrypt(urlsafe_b64decode(data_bin))
    #return json.dumps({'id': data['id'], 'data': str(urlsafe_b64encode(data_bin))})
    return json.dumps({'id': data['id'], 'data': data_bin})

@app.route("/decrypt", methods=['PUT'])
def decrypt():
    data = json.loads(request.data)
    data_bin = data['data']
    print(f"len data: {len(data_bin)}")
    #sleep(random.randrange(10))
    #result = fernet.decrypt(urlsafe_b64decode(data_bin))
    #return json.dumps({'id': data['id'], 'data': str(urlsafe_b64encode(data_bin))})
    return json.dumps({'id': data['id'], 'data': data_bin})

app.run(host="0.0.0.0")