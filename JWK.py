import json, requests

class JWK:
    def __init__(self):
        pub = requests.get('http://localhost:8000/pub.pem').text

        pub = pub[pub.find('\n')+1:pub.rfind('\n')]

        Obj = {}
        keys = []

        keys.append({   "alg": "RS256",
                        "kty": "RSA",
                        "use": "sig",
                        "kid": "http://localhost:8000/key.pem",
                        "x5c" : f"{pub}"
                    }
        )

        Obj["keys"] = keys

        with open('jwks1.json', 'w') as jwk:
            jwk.write(json.dumps(Obj, indent=4))
