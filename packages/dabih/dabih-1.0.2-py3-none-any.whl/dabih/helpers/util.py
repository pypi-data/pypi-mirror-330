from dabih.dabih_client.dabih_api_client.api.util import (
    healthy,
    info
)
from ..logger import dbg, error, warn
import json
import sys
import httpx

__all__ = ["healthy_func", "check_status"]

def healthy_func(client):

    try: 
        answer = healthy.sync_detailed(client=client)
    except httpx.ConnectError:
        error(f"Connection error: Please check the URL in config file or whether the server is running. \n Required format of base_url: http://<ip>:<port>")
        sys.exit(0)
        
    if not check_status(answer):
        return False
    else:
        return True

def check_status(answer, context = None):
    dbg("Checking Server Response...")

    if answer.status_code == 401:
        error("Token is unauthorized or expired")
        dbg(f"Server Response: {answer.content}")
        sys.exit(0)

    elif answer.status_code == 403:
        error("Not authorized to access this dabih folder/file")
        dbg(f"Server Response: {answer.content}")
        sys.exit(0)

    elif answer.status_code == 404:
        message = json.loads(answer.content)
        if context == "file_info":
            error(f"Requested dabih file/folder not found: {message['message']}. Only files, not folders, can be downloaded.")
        else:
            error(f"Requested dabih file/folder not found: {message['message']}.")
            warn("Dabih Files/Folders should always be refered to by their mnemonic. \nYou can use dabih search to check the mnemonic")
        dbg(f"Server Response: {answer.content}")
        sys.exit(0)

    elif answer.status_code == 500:
        try:
            response = json.loads(answer.content)
            dbg(f"Server Message: {response['message']}")
            if response["message"] == "jwt malformed":
                error("Token is malformed. Please check your token in the config file")
                sys.exit(0)
            else:
                error(f"Error with server message {response['message']}")
                sys.exit(0)
        except:
            error("Server Side Issue")
            dbg(f"Server Response: {answer.content}")
            return False

    elif answer.status_code == 200:
        dbg(f"Server Status Code: {answer.status_code}")
        dbg(f"Server Response: {answer.content}")
        if answer.content == b'[]':
            error("Folder is either empty or does not exist, please check the mnemonic")
            sys.exit(0)
        return True
    
    elif answer.status_code == 201:
        dbg(f"Server Status Code: {answer.status_code}")
        dbg(f"Server Response: {answer.content}")
        return True