import datetime
from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="Key")


@_attrs_define
class Key:
    """
    Attributes:
        id (Any): The database id of the key
        inode_id (Any): The inode id the key belongs to
        hash_ (str):
        key (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: Any
    inode_id: Any
    hash_: str
    key: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        inode_id = self.inode_id

        hash_ = self.hash_

        key = self.key

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "inodeId": inode_id,
                "hash": hash_,
                "key": key,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        inode_id = d.pop("inodeId")

        hash_ = d.pop("hash")

        key = d.pop("key")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        key = cls(
            id=id,
            inode_id=inode_id,
            hash_=hash_,
            key=key,
            created_at=created_at,
            updated_at=updated_at,
        )

        return key
