from flask import Flask, render_template, make_response, request, redirect
#from Crypto.PublicKey import RSA
from Crypto.Util.number import getStrongPrime, inverse
from Cryptodome.PublicKey import RSA
import requests
import jwt
import json, sys
import base64
from JWK import JWK


def pad(data):
    if len(data) % 8 != 0:
        data += b"=" * (8-len(data) % 8)
    return data

key = b'''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAuJdft62lNOkYM/uA26Rp6XWygVC+3r2TxtZnOqcbWpQ1RcDY
FibfJ93qwkigc2DB2T3PcbzxEbqZyqC1VJFeMQRaqtsiN6F/xfooYlh52mBfwq3Q
wRPB+NWcZsfRqcyu23Pp4tl0Ra1iw7h7pfbGsNlcnd90f9BZuvbkTeDFwkwoEUlE
5DSAmWODxGY4nMZNlZyUM9bxFQxrc1gKSF+O3TNeV3mWpXvL+OMG6W0MeuW5KCSs
Nk/9/o+Xkd5RNbQHNgeqV5A9tfl98/I67CPBZM8545mh3Wfw34o9DRX10cpvP9T2
VfkWQdzfZISKRXSOyE8TsL05pjuXW+uJZY2WiQIDAQABAoIBAAsdQiwjDnFzH3vx
xr5y1dWyun7Cx9tNetpcCncjnKgFiHectuYOjR0vZXUxPkf0KXfVGup0P+ebXqsu
pfxjjFJTOspSy2qiFLls6IWTYjLd3qYwJQObFvDOm84sddlNc7HO9uQrx65yVCII
t5k0lJ4NWGBBFhikCOMS/ogZ4o5iQU5CNVDxMtxAK5B8njWtv325Y0snQlh8HmzM
5IosHq2JBHwEvv393vdcT9+IJ9kVTHMde+4dGmmu5oLjVWw6E3HloVQsjup+6es6
twMZqtp2pvjWe89bNNKpL/Mn/HVhTBTMhpTNya2Iqo6ZlvKjuuIH66St1a+cvoBM
0OOZtgECgYEA4JrBLbVLlg9thuAGjiUeQNOuXKMITobcvcRROPIEvSdrXuDcrZba
nWSM7LUccNoqA3nsdglpgjKJEiWBZcZLSleSaKouHWh+j3Z04P5LgkrggM0Bv3me
r3xwSRwVL5EsdRp4UVXN9VPEmFeOwpzasHrXEgZCm8nuFcAnK9NfpGECgYEA0mTJ
g1JMctBZY74VysGeHOGIbPz782hExNl/6zfzOOKQuPDjjzic976NbSAzlXL8fG7n
sqIg96il1/WFQJSuLRscr7go9vknFcuwU/j1kshZzgLoB2EgDDKS14Dm2V308hhY
7ASvkuVhD/QrAeb3tbSy71UBqhfUszxQa46jIykCgYEAkTRbSXKYoDXvKDAy7Lig
e2aepfMcjq/vi5ucqwUD/Um7x4X2BR+uy+xSk0FvVqIkYUT0k0b4eBy1sw6ePi7Z
RAGjfJjw4UBJ+fOqEj80j9Jam8pto907stXvPcSzCaKALGDlgifH1B/IzHhmqfiA
BXIVEukLLO56RoOIj3PCtGECgYEAsOJxlUnM4j6O2M/ITIYJ46gt5cuwG82O+50M
8fpBL5M0L3i/KPtk5Nk82AFZvQ1Gf2tSuxmZ8/3DKNTPqiMWaO/BZ27CahnBJY7x
eTf3ZuewsQY6g3HB2t9uG2bRLvDSbfPQVuX9otfciegzfE7t9cOtKJBkbNfKSMKt
ri/msjkCgYANjuVNtAzH2sHbsXZVl8RJ6YmRBa8qRLoyXlba4laHp6ryxrzqL3HG
C2/Tf9qkwp4HIK6hfJRvicmbXR4ATLMxsgsOfSuCSrOPf7VNjbh3ewSH8wLYmguF
r1xERFBEE2jMVjcDsj14TnT1Xk9BMPKfda8CaQdElR/jTHWA8MEZUQ==
-----END RSA PRIVATE KEY-----'''

something = RSA.import_key(key)
# print(something.publickey().export_key('PEM'))


t = sys.argv[1].encode()

p = json.loads(base64.b64decode(t))
p['admin_cap'] = True
p = pad(json.dumps(p, indent=4).encode())
print(base64.b64encode(p))

