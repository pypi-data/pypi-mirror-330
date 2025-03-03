from dabih.dabih_client.dabih_api_client.api.filesystem import (
    list_home,
    list_files,
    file_info,
    list_inodes,
    list_parents, 
    search_fs,
    search_cancel,
    search_results
)
from dabih.dabih_client.dabih_api_client.models.inode_search_body import InodeSearchBody
from .json import decode_json   
from .util import check_status
from ..logger import dbg, warn, log, error

import time
import signal
import sys

__all__ = ["list_home_func", "list_files_func", "get_file_info", "search_func"]

def print_file_structure(items, indent=0):
    for item in items:
        print(f"{'    ' * indent}{item['name']:<30}\t{item['mnemonic']}")
        if 'children' in item:
            print_file_structure(item['children'], indent + 1)
    return None

def list_home_func(client):
    
    answer = list_home.sync_detailed(client=client)
    check_status(answer)
    response_json = decode_json(answer.content)
    
    parents = response_json.get('parents', [])
    children = response_json.get('children', [])

    parent_map = {parent['id']: parent for parent in parents}
    for child in children:
        parent_id = child['parentId']
        if parent_id in parent_map:
            if 'children' not in parent_map[parent_id]:
                parent_map[parent_id]['children'] = []
            parent_map[parent_id]['children'].append(child)

    log("\nHome Directory Structure:\n")
    print_file_structure(parents)
    print("")

    return None

def list_files_func(mnemonic, client):

    answer = list_files.sync_detailed(client=client, mnemonic=mnemonic)
    check_status(answer)
    response_json = decode_json(answer.content)
    if response_json[0]["mnemonic"] == mnemonic:
        warn(f"{mnemonic} refers to a file, not to a folder")
        sys.exit(0)

    log(f"\nFolder content of: {mnemonic}:\n")
    print_file_structure(response_json)
    print("")

    return None
    
def get_file_info(mnemonic, client):
    answer = file_info.sync_detailed(client = client, mnemonic = mnemonic)
    check_status(answer, context= "file_info")
    file = decode_json(answer.content)
    try:
        data = file["data"]
    except KeyError:
        error(f"File {mnemonic} not found, please check the mnemonic")
        sys.exit(0)
    uid = data["uid"]
    size = data["size"]
    key_list = file["keys"]

    return data, uid, key_list, size

def search_fs_func(client, query):
    search_body = InodeSearchBody(query)
    dbg(f"Search Body: {search_body}")
    answer = search_fs.sync_detailed(client = client, body = search_body)
    check_status(answer)
    decoded_answer = decode_json(answer.content)
    job_id = decoded_answer["jobId"]
    
    return job_id

def search_results_func(client, job_id):
    answer = search_results.sync_detailed(client = client, job_id = job_id)
    check_status(answer)
    return decode_json(answer.content)

def search_cancel_func(client, job_id):
    log("Cancelling current search.")
    answer = search_cancel.sync_detailed(client = client, job_id = job_id)
    check_status(answer)
    sys.exit(0)
    
def search_func(client, query):
    log("Searching...")
    job_id = search_fs_func(client, query)

    def signal_handler(sig, frame):
        search_cancel_func(client, job_id)
    signal.signal(signal.SIGINT, signal_handler)

    results = []

    while True:
        answer = search_results_func(client, job_id)
        results.append(answer["inodes"])

        if answer["isComplete"] is True:
            dbg(results)
            log("Search Results:")
            if results[0] == []:
                log(f"No matching files found for query: {query}")
            else:
                for result in results:
                    for inode in result:
                        name = inode.get("name")
                        mnemonic = inode.get("mnemonic")
                        created_at = inode.get("createdAt")
                        data = inode.get("data", {})
                        if data: 
                            size = data.get("size")
                            author = data.get("createdBy")
                            print(f"Name: {name}\n\tMnemonic: {mnemonic}\n\tCreated By: {author}\n\tCreated At: {created_at}\n\tSize: {size} MiB")
                        else:
                            print(f"Name: {name}\n\tMnemonic: {mnemonic}\n\tCreated At: {created_at}")

            break
        time.sleep(0.3)
