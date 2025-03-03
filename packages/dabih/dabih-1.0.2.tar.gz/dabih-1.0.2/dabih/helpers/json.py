import json
from ..logger import error

__all__=["decode_json", "print_json"]

def decode_json(answer):
    if not answer:
        error("Empty server response; please check if server is reachable")
        raise ValueError("No server response; please check if server is reachable")
    
    answer = answer.decode("utf-8")
    string = json.loads(answer)
    return string

def print_json(json_str):
    decoded_answer = decode_json(json_str)
    print(json.dumps(decoded_answer, indent=2))
