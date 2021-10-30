from flask import Flask, render_template, make_response, request, redirect
import requests, jwt, json, base64, sys
from secret import Secret

app = Flask(__name__)

payload = {
    'user': "guest",
    'admin_cap': 'false',
    'kid': "http://localhost:8000/secret.txt"
}

Obj = Secret()

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
    
    if user:
        payload['user'] = user
        encoded_jwt = jwt.encode(payload, requests.get(
            payload['kid']).text, algorithm='HS256')

        resp = make_response(render_template(
            "index.html", testing=encoded_jwt))

    else:
        # passing guest user as default user
        encoded_jwt = jwt.encode(payload, requests.get(
            payload['kid']).text, algorithm='HS256') 
        resp = make_response(render_template("index.html", testing=encoded_jwt))

    resp.set_cookie('token', encoded_jwt)
    return resp


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    token = request.cookies.get('token')
    if token:
        v = verify(token)
        resp = make_response(render_template("index.html", testing=v))
    else:
        return "No token"
    
    resp.set_cookie('token', token)
    return resp


def verify(token: str) -> str:
    token_split = token.split('.')[1].encode()
    token_split = pad(token_split)
    token_payload = base64.b64decode(token_split).decode()
    token_payload = json.loads(token_payload)
    
    kid = token_payload['kid']
    verification_sec = requests.get(kid).text
    
    try:
        dcoded_token = jwt.decode(token, verification_sec, algorithms=['HS256'])
    except:
        return "SIG_FAIL"
    
    if dcoded_token['admin_cap'] == 'false':
        return "Not valid"
    else:
        return "flag"


if __name__ == '__main__':
    app.run(debug=True)
