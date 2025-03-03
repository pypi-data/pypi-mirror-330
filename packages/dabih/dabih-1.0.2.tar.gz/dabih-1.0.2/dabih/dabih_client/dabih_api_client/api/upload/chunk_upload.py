from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chunk import Chunk
from ...models.chunk_upload_body import ChunkUploadBody
from ...types import Response


def _get_kwargs(
    mnemonic: str,
    *,
    body: ChunkUploadBody,
    content_range: str,
    digest: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["content-range"] = content_range

    headers["digest"] = digest

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/upload/{mnemonic}/chunk",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Chunk]:
    if response.status_code == 201:
        response_201 = Chunk.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Chunk]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    mnemonic: str,
    *,
    client: AuthenticatedClient,
    body: ChunkUploadBody,
    content_range: str,
    digest: str,
) -> Response[Chunk]:
    """
    Args:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        content_range (str):
        digest (str):
        body (ChunkUploadBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Chunk]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
        body=body,
        content_range=content_range,
        digest=digest,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    mnemonic: str,
    *,
    client: AuthenticatedClient,
    body: ChunkUploadBody,
    content_range: str,
    digest: str,
) -> Optional[Chunk]:
    """
    Args:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        content_range (str):
        digest (str):
        body (ChunkUploadBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Chunk
    """

    return sync_detailed(
        mnemonic=mnemonic,
        client=client,
        body=body,
        content_range=content_range,
        digest=digest,
    ).parsed


async def asyncio_detailed(
    mnemonic: str,
    *,
    client: AuthenticatedClient,
    body: ChunkUploadBody,
    content_range: str,
    digest: str,
) -> Response[Chunk]:
    """
    Args:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        content_range (str):
        digest (str):
        body (ChunkUploadBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Chunk]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
        body=body,
        content_range=content_range,
        digest=digest,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    mnemonic: str,
    *,
    client: AuthenticatedClient,
    body: ChunkUploadBody,
    content_range: str,
    digest: str,
) -> Optional[Chunk]:
    """
    Args:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        content_range (str):
        digest (str):
        body (ChunkUploadBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Chunk
    """

    return (
        await asyncio_detailed(
            mnemonic=mnemonic,
            client=client,
            body=body,
            content_range=content_range,
            digest=digest,
        )
    ).parsed
