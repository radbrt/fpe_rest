# app.py - a minimal flask api using flask_api
from flask import request
from flask_api import FlaskAPI, status, exceptions
import random, codecs, os
from flask_cors import CORS
import pyffx
import string

app = FlaskAPI(__name__)
CORS(app)

tokendefinitions = {
    'FNR': {'alphabet': string.digits,
            'length': 11},
    'REG': {'alphabet': string.ascii_lowercase + string.digits,
            'length': 7}
}

def encrypt_object(encryptstring, piidef):
    key = bytearray(os.getenv("FFXKEY").encode('utf-8'))

    if piidef in tokendefinitions.keys():
        ffx = pyffx.String(key, 
            alphabet=tokendefinitions[piidef]['alphabet'], 
            length=tokendefinitions[piidef]['length'])
        try:
            encrypted_string = ffx.encrypt(encryptstring)
            return({'status': 'success', 'string': encrypted_string})
        except Exception as e:
            return({'status': 'error', 'string': '', 'message': e})

def encrypt_array(encryptstrings, ffxengine):
    try:
        pseudonyms = {"status": "success", "payload": [ffxengine.encrypt(pii) for pii in encryptstrings]}
    except Exception as e:
        pseudonyms = {"status": "error", "message": e}
    
    return(pseudonyms)

@app.route('/encrypt', methods=['POST'])
def encrypt_json():
    if not "FFXKEY" in os.environ:
        return("Incorrectly configured server: No encryption key", 500)

    piidata = request.data.get('data')
    encrypted_data = [encrypt_object(p['string'], p['tokentype']) for p in piidata]
    return({'result': encrypted_data})


@app.route('/bulkencrypt', methods=['POST'])
def bulkencrypt():
    if not "FFXKEY" in os.environ:
        return("Incorrectly configured server: No encryption key", status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    key = bytearray(os.getenv("FFXKEY").encode('utf-8'))

    piidata = request.data.get('data')
    ffx = pyffx.String(key, 
                alphabet=tokendefinitions[piidata['tokentype']]['alphabet'], 
                length=tokendefinitions[piidata['tokentype']]['length'])

    encrypted_data = encrypt_array(piidata['payload'], ffx)
    if encrypted_data["status"]=="success":
        return(encrypted_data)
    else:
        return("Bulk encryption failed, status not success", status.HTTP_409_CONFLICT)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if not "FFXKEY" in os.environ:
        return("Incorrectly configured server: No encryption key", 500)
    else:
        return("Sorry, I haven't learned how to do that yet", status.HTTP_501_NOT_IMPLEMENTED)

@app.route('/')
def generalresponse():
    if not "FFXKEY" in os.environ:
        return("Incorrectly configured server: No encryption key", 500)
    else:
        return({'whoami': 'a placeholder encryption service at your service'})

@app.errorhandler(500)
def internal_error(error):
    return("500 Server error. Please check your input", status.HTTP_500_INTERNAL_SERVER_ERROR)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)