# decryption
from cryptography.hazmat.primitives import hashes, ciphers, padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import algorithms, modes
from cryptography.hazmat.backends import default_backend

from .b64 import decode as b64_decode

def decrypt_aes_key(encrypted_aes_key, private_key):
    encrypted_aes_key_bytes = b64_decode(encrypted_aes_key)
    decrypted_aes_key = private_key.decrypt(
        encrypted_aes_key_bytes,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted_aes_key


def decrypt_file_chunk(chunk_data, aes_key, iv):
    cipher = ciphers.Cipher(
        algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend()
    )
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(chunk_data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return unpadded_data
