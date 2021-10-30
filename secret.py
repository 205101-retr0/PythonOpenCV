import os

class Secret:
    def __init__(self):
        secret = os.urandom(20)

        with open('secret.txt', 'wb') as f:
            f.write(secret)
        
