from flask import Flask, request
from time import sleep 
import random
from cryptography.fernet import Fernet

from base64 import urlsafe_b64encode, urlsafe_b64decode

import json

# Fernet
fernet = Fernet("oYiV_ftSLe-YQjo9UqOWq0KGeiU1ovtCmBeV4XHaWew=")

app = Flask(__name__)

@app.route("/status")
def status():
    return "<p>I exist!</p>"

@app.route("/encrypt", methods=['PUT'])
def encrypt():
    data = json.loads(request.data)
    data_str = data['data']
    print(f"len data_str: {len(data_str)}")
    data_bin = str.encode(data_str, "utf-8")
    data_bytes = urlsafe_b64decode(data_bin)
    #print(data_bin)
    #sleep(random.randrange(10))
    result = fernet.encrypt(data_bytes)

    result_safe_bytes = urlsafe_b64encode(result)
    result_str = str(result_safe_bytes, "utf-8")
    return json.dumps({'id': data['id'], 'data': result_str})
    #return json.dumps({'id': data['id'], 'data': data_bin})

@app.route("/decrypt", methods=['PUT'])
def decrypt():
    data = json.loads(request.data)
    data_str = data['data']
    print(f"len data: {len(data_str)}")
    data_bytes_safe = str.encode(data_str, "utf-8")
    data_bytes = urlsafe_b64decode(data_bytes_safe)
    #sleep(random.randrange(10))
    result = fernet.decrypt(data_bytes)

    result_bytes_safe = urlsafe_b64encode(result)
    result_str = str(result_bytes_safe, "utf-8")

    return json.dumps({'id': data['id'], 'data': result_str})
    #return json.dumps({'id': data['id'], 'data': data_bin})

app.run(host="0.0.0.0")