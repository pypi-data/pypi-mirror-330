import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="Chunk")


@_attrs_define
class Chunk:
    """
    Attributes:
        id (Any): The database id of the chunk
        data_id (Any): The id of the data the chunk belongs to
        hash_ (str): The SHA-256 hash of the unencrypted chunk data base64url encoded
        iv (str): The AES-256 initialization vector base64url encoded
        start (Any): The start of the chunk as a byte position in the file
        end (Any): The end of the chunk as a byte position in the file
        crc (Union[None, str]): The CRC32 checksum of the encrypted chunk data base64url encoded
        created_at (datetime.datetime): chunk creation timestamp
        updated_at (datetime.datetime): chunk last update timestamp
    """

    id: Any
    data_id: Any
    hash_: str
    iv: str
    start: Any
    end: Any
    crc: Union[None, str]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        data_id = self.data_id

        hash_ = self.hash_

        iv = self.iv

        start = self.start

        end = self.end

        crc: Union[None, str]
        crc = self.crc

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "dataId": data_id,
                "hash": hash_,
                "iv": iv,
                "start": start,
                "end": end,
                "crc": crc,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        data_id = d.pop("dataId")

        hash_ = d.pop("hash")

        iv = d.pop("iv")

        start = d.pop("start")

        end = d.pop("end")

        def _parse_crc(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        crc = _parse_crc(d.pop("crc"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        chunk = cls(
            id=id,
            data_id=data_id,
            hash_=hash_,
            iv=iv,
            start=start,
            end=end,
            crc=crc,
            created_at=created_at,
            updated_at=updated_at,
        )

        return chunk
