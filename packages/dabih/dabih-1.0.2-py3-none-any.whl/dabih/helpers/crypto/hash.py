import hashlib
from .b64 import decode as b64_decode 
from .b64 import encode as b64_encode
from cryptography.hazmat.primitives import hashes, serialization

def get_key_hash(key):
    public_key = key.public_key()
    spki = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    digest = hashes.Hash(hashes.SHA256())
    digest.update(spki)

    hashed = digest.finalize()
    base64url_hash = b64_encode(hashed)
    return base64url_hash


def get_chunk_hash(chunk_data):
    sha256_hash = hashlib.sha256(chunk_data).digest()
    return b64_encode(sha256_hash)

def get_full_chunk_hash(hash_list):
    hash = hashlib.sha256()
    for b64 in hash_list:
        buffer = b64_decode(b64)
        hash.update(buffer)
    return b64_encode(hash.digest())
