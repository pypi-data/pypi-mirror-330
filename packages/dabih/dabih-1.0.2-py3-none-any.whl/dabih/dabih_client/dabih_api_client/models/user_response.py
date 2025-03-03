import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.public_key import PublicKey


T = TypeVar("T", bound="UserResponse")


@_attrs_define
class UserResponse:
    """
    Attributes:
        id (Any): The database id of the user
        sub (str): The unique user sub
        name (str): The name of the user
        email (str): The email of the user
        created_at (datetime.datetime): The date the user was created
        updated_at (datetime.datetime): The date the user was last updated
        keys (List['PublicKey']): The public keys of the user
    """

    id: Any
    sub: str
    name: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    keys: List["PublicKey"]

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        sub = self.sub

        name = self.name

        email = self.email

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        keys = []
        for keys_item_data in self.keys:
            keys_item = keys_item_data.to_dict()
            keys.append(keys_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "sub": sub,
                "name": name,
                "email": email,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "keys": keys,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.public_key import PublicKey

        d = src_dict.copy()
        id = d.pop("id")

        sub = d.pop("sub")

        name = d.pop("name")

        email = d.pop("email")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        keys = []
        _keys = d.pop("keys")
        for keys_item_data in _keys:
            keys_item = PublicKey.from_dict(keys_item_data)

            keys.append(keys_item)

        user_response = cls(
            id=id,
            sub=sub,
            name=name,
            email=email,
            created_at=created_at,
            updated_at=updated_at,
            keys=keys,
        )

        return user_response
