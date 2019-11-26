# app.py - a minimal flask api using flask_api
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import random, codecs, os
from flask_cors import CORS
import pyffx
import string

# TODO: refactor API design

tokendefinitions = {
    'FNR': {'alphabet': string.digits,
            'length': 11},
    'SNR': {'alphabet': string.ascii_lowercase + string.digits,
            'length': 7}
}

def encrypt_string(encryptstring, piidef):
    key = os.getenv("FFXKEY")

    if piidef in tokendefinitions.keys():
        ffx = pyffx.String(key, 
            alphabet=tokendefinitions[piidef]['alphabet'], 
            length=tokendefinitions[piidef]['length'])
        try:
            encrypted_string = ffx.encrypt(encryptstring)
            return({'status': 'success', 'string': encrypted_string})
        except: # TODO: Check for error types
            return({'status': 'error', 'string': '', 'message': 'Failed to encrypt string'})


app = FlaskAPI(__name__)
CORS(app)

app.debug = False

@app.route('/encrypt', methods=['POST'])
def encrypt_json():
    if not "FFXKEY" in os.environ:
        return("Incorrectly configured server: No encryption key", 500)

    piidata = request.data.get('data')
    encrypted_data = [encrypt_string(p['string'], p['tokentype']) for p in piidata]
    return({'result': encrypted_data})


@app.route('/decrypt')
def getinit():
    if not "FFXKEY" in os.environ:
        return("Incorrectly configured server: No encryption key", 500)
    else:
        return({'error': "sorry, i haven't learned to do that yet :("})

@app.route('/')
def generalresponse():
    if not "FFXKEY" in os.environ:
        return("Incorrectly configured server: No encryption key", 500)
    else:
        return({'whoami': 'a placeholder encryption service at your service'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')