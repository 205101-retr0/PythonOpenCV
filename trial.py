from flask import Flask, render_template, make_response, request
from Crypto.PublicKey import RSA
from Crypto.Util.number import getStrongPrime,inverse
import requests
import jwt, json
from JWK import JWK

app = Flask(__name__)

# key = RSA.generate(1024)

p = getStrongPrime(1024)
q = getStrongPrime(1024)
n = p*q
e = 65537
d = inverse(e, (p-1)*(q-1))
key = RSA.construct((n, e, d, p, q), True)

# Generating the Private Key
f = open('key.pem', 'wb')
f.write(key.export_key('PEM'))
f.close()


## Generating the Public Key
f = open('pub.pem', 'wb')
f.write(key.publickey().export_key('PEM'))
f.close()

# pub_key = key.publickey().export_key('PEM').decode()


################################ THIS WORKS NOW ####################################
priv_key = requests.get('http://localhost:8000/key.pem').text.encode()
####################################################################################

##################################### THIS WORKS ###################################
# priv_key = key.exportKey("PEM").decode()
####################################################################################

url = "http://localhost:8000/jwks1.json"
Obj = JWK()
jwk = (requests.get(url).json())
pub_key = jwk['keys'][0]['x5c']
pub_key = ('-----BEGIN PUBLIC KEY-----\n' +
           pub_key + '\n-----END PUBLIC KEY-----')
# print(pub_key)

# pub_key = requests.get('http://localhost:8000/pub.pem').text
# print(pub_key)

# print(f'PRIVATE --> {priv_key}\nPUBLIC --> {pub_key}')

encoded_jwt = jwt.encode({'some': 'payload'}, priv_key, algorithm='RS256')
# print(encoded_jwt)

@app.route('/')
def index():
    return render_template('index.html', testing=encoded_jwt)

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = request.form['username']
    payload = {
        'user' : user
    }
    ## Yes you get the KID as the header for now, BUT Do you really NEED the KID??
    encoded_jwt = jwt.encode(payload, priv_key, algorithm='RS256')
    print(f"{encoded_jwt}")
    dcodec_jwt = jwt.decode(encoded_jwt, pub_key, algorithms='RS256')
    print(f'{dcodec_jwt}')
    # return 'IT WORKED'
    return render_template('index.html', testing=f"{dcodec_jwt}")

if __name__ == '__main__':
    app.run(debug=True)
    # pass
