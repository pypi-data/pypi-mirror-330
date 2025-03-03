import base64

def decode(iv):
    iv += '=' * (-len(iv) % 4)
    iv = base64.urlsafe_b64decode(iv)
    return iv

def encode(iv):
    iv = base64.urlsafe_b64encode(iv).rstrip(b'=').decode('utf-8')
    return iv
