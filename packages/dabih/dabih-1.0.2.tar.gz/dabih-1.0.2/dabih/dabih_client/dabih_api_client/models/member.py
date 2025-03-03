import datetime
from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.permission import Permission

T = TypeVar("T", bound="Member")


@_attrs_define
class Member:
    """
    Attributes:
        id (Any): The database id of the member
        sub (str):
        inode_id (Any): The database id of the inode
        permission (Permission): The Permission type is used to represent the permissions a user has on a Inode.
            NONE: No permissions
            READ: user may only read the file or directory
            WRITE: user can read, share, edit, and delete the file or directory
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: Any
    sub: str
    inode_id: Any
    permission: Permission
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        sub = self.sub

        inode_id = self.inode_id

        permission = self.permission.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "sub": sub,
                "inodeId": inode_id,
                "permission": permission,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        sub = d.pop("sub")

        inode_id = d.pop("inodeId")

        permission = Permission(d.pop("permission"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        member = cls(
            id=id,
            sub=sub,
            inode_id=inode_id,
            permission=permission,
            created_at=created_at,
            updated_at=updated_at,
        )

        return member
