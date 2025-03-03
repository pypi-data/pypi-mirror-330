import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="FileData")


@_attrs_define
class FileData:
    """
    Attributes:
        id (Any): The database id of the file data
        uid (str):
        created_by (str):
        file_name (str):
        file_path (Union[None, str]):
        hash_ (Union[None, str]):
        size (Any): The size of the file in bytes
        key_hash (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: Any
    uid: str
    created_by: str
    file_name: str
    file_path: Union[None, str]
    hash_: Union[None, str]
    size: Any
    key_hash: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        uid = self.uid

        created_by = self.created_by

        file_name = self.file_name

        file_path: Union[None, str]
        file_path = self.file_path

        hash_: Union[None, str]
        hash_ = self.hash_

        size = self.size

        key_hash = self.key_hash

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "uid": uid,
                "createdBy": created_by,
                "fileName": file_name,
                "filePath": file_path,
                "hash": hash_,
                "size": size,
                "keyHash": key_hash,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        uid = d.pop("uid")

        created_by = d.pop("createdBy")

        file_name = d.pop("fileName")

        def _parse_file_path(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        file_path = _parse_file_path(d.pop("filePath"))

        def _parse_hash_(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        hash_ = _parse_hash_(d.pop("hash"))

        size = d.pop("size")

        key_hash = d.pop("keyHash")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        file_data = cls(
            id=id,
            uid=uid,
            created_by=created_by,
            file_name=file_name,
            file_path=file_path,
            hash_=hash_,
            size=size,
            key_hash=key_hash,
            created_at=created_at,
            updated_at=updated_at,
        )

        return file_data
