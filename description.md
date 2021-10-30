## What's supposed to Happen:
JWKS.json contains the url for private key and contains the public key for certificate verification. \
\
So, The code's supposed to get the private key from the KID and use the public key for verfication from the same.\
\
OR MAYBE NOT ( not sure about this but maybe if avoid putting private key url in the jwks.json we may be able to build this more easily. )\
MAYBE NOT\
\
This what it's supposed to be.

## Expoilt:
Making a public and private key on our own server and redirecting a private key and public key get request to our own machine.\
\
So, we can veriy and sign our own JWT token.\
Basically we take the ctf ka server out of the equation for token generation.