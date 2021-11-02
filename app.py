from flask import Flask, render_template, make_response, request, redirect
import requests, jwt, json, base64, os
from secret import Secret
from dotenv import load_dotenv

load_dotenv()
FLAG = os.environ.get("FLAG")

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
    return render_template('index.html', output="HIT THIS TO GET TOKEN...")


@app.route('/generateToken', methods=['GET', 'POST'])
def generateToken():
    user = request.form['username']
    
    if user:
        payload['user'] = user
        encoded_jwt = jwt.encode(payload, requests.get(
            payload['kid']).text, algorithm='HS256')

        resp = make_response(render_template(
            "index.html", output=encoded_jwt))

    else:
        # passing guest user as default user
        encoded_jwt = jwt.encode(payload, requests.get(
            payload['kid']).text, algorithm='HS256') 
        resp = make_response(render_template("index.html", output=encoded_jwt))

    resp.set_cookie('token', encoded_jwt)
    return resp


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    token = request.cookies.get('token')
    if token:
        val = verify(token)
        if val == "SIG_FAIL":
            resp = make_response(render_template("home"), result = "Signature Verification Failure")
        elif val == "N_ADMIN":
            resp = make_response(render_template("home"), result="No Admin Capabilities Found")
        elif val == "ALL_CHECKS_PASSED":
            resp = make_response(render_template("home"), result=FLAG)
    else:
        resp = make_response(render_template("home"), result="No Token Was Set!")
    
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
        return "N_ADMIN"
    else:
        return "ALL_CHECKS_PASSED"


if __name__ == '__main__':
    app.run(debug=True)
