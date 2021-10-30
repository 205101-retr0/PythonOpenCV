from flask import Flask, render_template, make_response, request, redirect
from Crypto.PublicKey import RSA
from Crypto.Util.number import getStrongPrime, inverse
import requests, jwt, json, base64, sys
from JWK import JWK

app = Flask(__name__)

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


## Default Payload we gonna be sending...
payload = {
    'user': "guest",
    'admin_cap': 'false',
    'kid': "http://localhost:8000/key.pem"
}

url = "http://localhost:8000/jwks.json"

Obj = JWK()
jwk = requests.get(url).json()
pub_key = jwk['keys'][0]['x5c']
pub_key = ('-----BEGIN PUBLIC KEY-----\n' +
           pub_key + '\n-----END PUBLIC KEY-----')


def pad(data):
    if len(data) % 8 != 0:
        data += b"=" * (8-len(data) % 8)
    return data


@app.route('/')
def index():
    return render_template('index.html', testing="HIT THIS TO GET TOKEN...")


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = request.form['username']
    token = request.cookies.get('token')

    payload['user'] = user

    if token:
        token_split = token.split('.')[1].encode()
        token_split = pad(token_split)
        token_payload = base64.b64decode(token_split).decode()
        token_payload = json.loads(token_payload)
        token_payload['user'] = user
        
        try:
            priv_key = requests.get(token_payload['kid']).text.encode()
        except:
            print("Error Getting the key")
            sys.exit(0)
        
        # encoded_jwt = jwt.encode(token_payload, priv_key, algorithm='RS256')

        ## IT'S MORE MESSY THAN I THOUGHT................
        # GO TO A NEW FUNCTION `verify()` WHERE WE GENERATE A PUBLIC KEY USING THE PRIVATE KEY GIVEN AND THEN USE THAT TO VERIFY 
        # ADMIN AND SHIT.
        # FIX THE FLOW OF CODE.

        v = verify(priv_key, token)
        
        return v

        # return redirect('/verify')
    else:
        encoded_jwt = jwt.encode(payload,"secret", algorithm='HS256')

        resp = make_response(render_template("index.html", testing=encoded_jwt))

        resp.set_cookie('token', encoded_jwt)

    return resp


def verify(priv_key: bytes, token: str) -> str:
    key = RSA.importKey(priv_key)

    # THIS KEY MIGHT NOT BE THE SAME AS THE FILE ONE.
    # THIS IS PROBLEM. IT DEFEATS THE PURPOSE FO THE CHALL.
    # THINK OF SOMETHING ELSE.
    pub_key = key.publickey().export_key('PEM')
    print(pub_key)
    print("Works till here..")
    try:
        dcodec_jwt = jwt.decode(token, pub_key, algorithms=['RS256'])
    except:
        return "SIG_FAIL"
    
    if dcodec_jwt['admin_cap'] == 'true':
        return "IT WORKS"

    return token


if __name__ == '__main__':
    app.run(debug=True)


#### TODO:
# Get url to jwks.json from KID param in payload.
# Then the public key to the key will be in jwks.json
# we make a private key and public key on our machine
# and re-direct the url to our machine. so we can a token with admin_cap = 1
# and re-direct them from their server to ours and then
# we can sign it with our priv key and verify it our pub key.
