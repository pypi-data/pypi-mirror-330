from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.decrypt_dataset_body import DecryptDatasetBody
from ...models.token_response import TokenResponse
from ...types import Response


def _get_kwargs(
    mnemonic: str,
    *,
    body: DecryptDatasetBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/download/{mnemonic}/decrypt",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TokenResponse]:
    if response.status_code == 200:
        response_200 = TokenResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TokenResponse]:
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
    body: DecryptDatasetBody,
) -> Response[TokenResponse]:
    """
    Args:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        body (DecryptDatasetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenResponse]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    mnemonic: str,
    *,
    client: AuthenticatedClient,
    body: DecryptDatasetBody,
) -> Optional[TokenResponse]:
    """
    Args:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        body (DecryptDatasetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TokenResponse
    """

    return sync_detailed(
        mnemonic=mnemonic,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    mnemonic: str,
    *,
    client: AuthenticatedClient,
    body: DecryptDatasetBody,
) -> Response[TokenResponse]:
    """
    Args:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        body (DecryptDatasetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenResponse]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    mnemonic: str,
    *,
    client: AuthenticatedClient,
    body: DecryptDatasetBody,
) -> Optional[TokenResponse]:
    """
    Args:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        body (DecryptDatasetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TokenResponse
    """

    return (
        await asyncio_detailed(
            mnemonic=mnemonic,
            client=client,
            body=body,
        )
    ).parsed
