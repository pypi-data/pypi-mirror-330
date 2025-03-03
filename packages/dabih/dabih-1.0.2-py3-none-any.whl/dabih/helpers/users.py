from dabih.dabih_client.dabih_api_client.api.user import me
from .json import decode_json
from .crypto import hash
from .token import get_token_info
from .util import healthy_func, check_status
from ..logger import dbg, warn, log, error
from cryptography.hazmat.primitives import serialization
import httpx
import sys

__all__=["get_user_info", "get_user_key_files", "check_user_credentials"]

def get_user_info(client):
    dbg("getting user info...")
    try:
        answer = me.sync_detailed(client = client)
    except httpx.ConnectError:
        error(f"Connection error: Please check the URL in config file or whether the server is running. \n Required format of base_url: http://<ip>:<port>")
        sys.exit(0)
    except:
        error(f"Unknown connection error: Please check the URL in config file or whether the server is running. \n Required format of base_url: http://<ip>:<port>")
        sys.exit(0)
    check_status(answer)

    data = decode_json(answer.content)
    key_list = data["keys"]
    id = data["id"]
    name = data["name"]
    dbg(f"User ID: {id}, Name: {name}, Key List: {key_list}")
    return key_list, name

def get_user_key_files(key_list, pem_files):
    dbg("getting user specific key files...")
    dbg(f"Key List: {key_list}\nPem Files: {pem_files}")
    for pem_file in pem_files:
        pem_file_obj = open(pem_file, "rb")
        try:
            private_key = serialization.load_pem_private_key(
                pem_file_obj.read(),
                password=None 
            )
            pem_hash = hash.get_key_hash(private_key)
        except ValueError:
            warn(f"Error loading key from PEM file {pem_file}\nThis key file has an invalid format. Using another key if available.")
            pem_file_obj.close()
            pem_files.remove(pem_file)
            continue
        finally:
            pem_file_obj.close()

        if pem_hash not in [key["hash"] for key in key_list]:
            pem_files.remove(pem_file)

    return pem_files

def check_user_credentials(client, pem_files):
    
    *_, name = get_user_info(client)
    log(f"User name: {name}")

    if not pem_files:
        error(f"No valid key files for user with name {name} found")
    else:
        log(f"Found {len(pem_files)} valid key files for user with name {name}: {pem_files}")
    
    get_token_info(client)