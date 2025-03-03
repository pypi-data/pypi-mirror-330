from dabih.dabih_client.dabih_api_client.api.token import (
    token_info,
    add_token,
    list_tokens,
    remove_token, 
    )
from ..logger import dbg, warn, log, error
from .util import check_status
from .json import decode_json

__all__= ["get_token_info", "check_token_validity"]


def get_token_info(client):
    answer = token_info.sync_detailed(client=client)
    check_status(answer)
    info = decode_json(answer.content)
    log(f"Current Token is authorized for User {info['sub']} with the Scopes: {info['scopes']}")
    return None

def check_token_validity(client):
    answer = token_info.sync_detailed(client=client) 
    if check_status(answer):
        return True
    else:
        return False