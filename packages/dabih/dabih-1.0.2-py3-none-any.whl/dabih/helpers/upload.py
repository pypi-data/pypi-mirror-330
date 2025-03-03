from dabih.dabih_client.dabih_api_client.api.upload import (
    start_upload,
    chunk_upload,
    finish_upload,
    cancel_upload,
    unfinished_uploads,
)
from dabih.dabih_client.dabih_api_client.types import File
from dabih.dabih_client.dabih_api_client.models.upload_start_body import UploadStartBody
from dabih.dabih_client.dabih_api_client.models.chunk_upload_body import ChunkUploadBody

from .json import decode_json
from .crypto import hash
from .util import check_status
from ..logger import dbg, warn, log, error

from io import BytesIO
from pathlib import Path
import sys
import os


__all__ = ["upload_func"]

def start_upload_func(file_path, size, client, directory = None):

    file_name = os.path.basename(file_path)
    if directory is None: 
        body = UploadStartBody(file_name=file_name, size=size)
    else:
        body = UploadStartBody(file_name=file_name, size=size, directory=directory)
    dbg(f"Upload Body: {body}")

    answer = start_upload.sync_detailed(client=client, body=body)
    check_status(answer)
    return answer

def upload_chunk(mnemonic, chunk_data, start, end, total_size, client):
    
    log(f"Preparing to upload chunk from {start} to {end}")

    file_instance = File(payload=BytesIO(chunk_data), file_name="chunk", mime_type=None)
    dbg(f"File Instance: {file_instance}")
    body = ChunkUploadBody(chunk=file_instance)
    dbg(f"Chunk Upload Body: {body}")

    content_range = f"bytes {start}-{end}/{total_size}"
    digest = f"sha-256={hash.get_chunk_hash(chunk_data)}"

    response = chunk_upload.sync_detailed(
        mnemonic=mnemonic,
        client=client,
        body=body,
        content_range=content_range,
        digest=digest,
    )
    check_status(response)

    return response


def finish_upload_func(mnemonic, client):

    answer = finish_upload.sync_detailed(client=client, mnemonic=mnemonic)
    check_status(answer)
    result_hash = decode_json(answer.content)["data"]["hash"]
    return result_hash


def upload_func(filepath, client, target_directory=None):

    total_size = Path(filepath).stat().st_size
    chunk_size = 2 * 1024 * 1024
    start = 0

    start_upload_answer = start_upload_func(filepath, total_size, client, target_directory)
    mnemonic = decode_json(start_upload_answer.content)["mnemonic"]

    log(f"Upload started with mnemonic: {mnemonic}")
    hashes = []

    with open(filepath, "rb") as f:
        log("Uploading... 0%")
        while True:
            chunk_data = f.read(chunk_size)
            n = len(chunk_data)
            if n == 0:
                break
            end = start + n - 1
            chunk_answer = upload_chunk(
                mnemonic, chunk_data, start, end, total_size, client
            )
            last_percent = (start * 100) // total_size
            start += n
            percent = (start * 100) // total_size
            if percent != last_percent:
                log(f"{percent}%  ")
                sys.stdout.flush()
            chunk_hash = decode_json(chunk_answer.content)["hash"]
            hashes.append(chunk_hash)
            dbg(f"hashlist from server: {hashes}")

    result_hash = finish_upload_func(mnemonic, client)
    
    full_hash = hash.get_full_chunk_hash(hashes)
    if result_hash != full_hash:
        error(
            f"Upload failed: Hashes do not match: {result_hash} != {full_hash}"
        )
    log("Upload finished.")