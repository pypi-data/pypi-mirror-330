from dabih.dabih_client.dabih_api_client.api.download import download_chunk
from .filesystem import get_file_info
from .crypto import b64, decrypt, hash
from ..logger import dbg, warn, log, error
from .util import check_status
from cryptography.hazmat.primitives import serialization
import sys
import os

__all__ = ["find_key", "download_func"]


def find_key(key_list, pem_files):
    dbg("Finding private key...")
    dbg(f"key_list: {key_list}")
    for key in key_list:
        dbg(f"pem_list: {pem_files}")
        for pem_file in pem_files:
            try:
                with open(pem_file, "rb") as pem_file:
                    private_key = serialization.load_pem_private_key(
                        pem_file.read(),
                        password=None 
                    )
                    pem_hash = hash.get_key_hash(private_key)
            except (ValueError, TypeError) as e:
                warn(f"Error loading this PEM file {pem_file}. Using another key if available...")
                continue
                
            if key["hash"] == pem_hash:
                log("Found valid key")
                return private_key, key
            else:
                dbg(f"pem_hash: {pem_hash}")
                dbg(f"key_hash: {key['hash']}")

    warn("No valid key found")
    return None


def download_func(mnemonic, client, pem_files, target_dir = None):
    log(f"Starting download for mnemonic: {mnemonic}")
    file, uid, key_list, size = get_file_info(mnemonic, client)
    if not pem_files:
        error("No valid key files found. You need your private key to download files. \nDownload aborted.\nPlease check the README for instructions on where to store your private key.")
        sys.exit(0)
    private_key, aes_key_info = find_key(key_list, pem_files)
    
    if not private_key:
        error("No private key found for requested file. Please check your key files.")
        sys.exit(0)

    encrypted_aes_key = aes_key_info["key"]
    aes_key = decrypt.decrypt_aes_key(encrypted_aes_key, private_key)

    start = 0
    size = float(size)

    file_name = file["fileName"]
    if target_dir:
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, file_name)
    else:
        file_path = file_name
    
    with open(file_path, "wb") as f:
        log("Downloading... 0%")
        for chunk in file["chunks"]:

            chunk_hash = chunk["hash"]
            chunk_response = download_chunk.sync_detailed(uid=uid, hash_=chunk_hash, client=client)
            check_status(chunk_response)
            encrypted_chunk = chunk_response.content
        
            iv = b64.decode(chunk["iv"])
            decrypted_chunk = decrypt.decrypt_file_chunk(encrypted_chunk, aes_key, iv)
            n = len(decrypted_chunk)

            f.write(decrypted_chunk)

            last_percent = (start * 100) // size
            start += n
            percent = (start * 100) // size
            if percent != last_percent:
                log(f"{percent}%  ")
                sys.stdout.flush()

    absolute_file_path = os.path.abspath(file_path)
    log(f"Download finished.\nFile saved to {absolute_file_path}")