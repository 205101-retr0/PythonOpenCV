from flask import Flask, render_template, jsonify, request, make_response
import jwt
import datetime
from jwt import PyJWKClient
from cryptography.hazmat.primitives import serialization as crypto_serialization


app = Flask(__name__)
with open('priv.rsa') as f:
    key = f.read()
with open('pub.rsa') as f:
    pub = f.read()

@app.route('/')
def index():
    return

@app.route('/login')
def login():
    auth = request.authorization
    payload = {
    'user' : "something",
    'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    if auth and auth.password == "pass":
        token = jwt.encode(payload, key, algorithm='RS256', headers={"kid": "1"})
        # token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik5FRTFRVVJCT1RNNE16STVSa0ZETlRZeE9UVTFNRGcyT0Rnd1EwVXpNVGsxUWpZeVJrUkZRdyJ9.eyJpc3MiOiJodHRwczovL2Rldi04N2V2eDlydS5hdXRoMC5jb20vIiwic3ViIjoiYVc0Q2NhNzl4UmVMV1V6MGFFMkg2a0QwTzNjWEJWdENAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vZXhwZW5zZXMtYXBpIiwiaWF0IjoxNTcyMDA2OTU0LCJleHAiOjE1NzIwMDY5NjQsImF6cCI6ImFXNENjYTc5eFJlTFdVejBhRTJINmtEME8zY1hCVnRDIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.PUxE7xn52aTCohGiWoSdMBZGiYAHwE5FYie0Y1qUT68IHSTXwXVd6hn02HTah6epvHHVKA2FqcFZ4GGv5VTHEvYpeggiiZMgbxFrmTEY0csL6VNkX1eaJGcuehwQCRBKRLL3zKmA5IKGy5GeUnIbpPHLHDxr-GXvgFzsdsyWlVQvPX2xjeaQ217r2PtxDeqjlf66UYl6oY6AqNS8DH3iryCvIfCcybRZkc_hdy-6ZMoKT6Piijvk_aXdm7-QQqKJFHLuEqrVSOuBqqiNfVrG27QzAPuPOxvfXTVLXL2jek5meH6n-VWgrBdoMFH93QEszEDowDAEhQPHVs0xj7SIzA"
        url = "http://localhost:9000/jwks.json"
        jwks_client = PyJWKClient(url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        dcoded = jwt.decode(token, signing_key.key, algorithms=["RS256"], options={"verify_exp": False})
        # return jsonify({'token': token})
        return jsonify({'dcode': dcoded})

    return make_response("Doesn't exsist", 401, {'WWW-Authenticate' : 'Basic realm = "Login Req"'})


if __name__ == '__main__':
    app.run(debug=True)


    #   "n": "6d075d28dde003bbc252f9475a788425e6658398fbf9216beea01f7a436830d07804d72f6bbf6cefa89c8f8e719f445bbd0c7f2100cc6dd4a480a0dd1e7b65f247d76bf81e2ecb92220f034a69f573b2400fc47e8aa1a3b033ab543c4ea142094e6849f9f0afb51bae16dcd4ad9739722e76bdd931220c877ad9dc96e4e9415f",
    #   "e": "AQAB",