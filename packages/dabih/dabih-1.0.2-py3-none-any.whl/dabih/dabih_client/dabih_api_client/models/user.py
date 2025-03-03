from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """User is the type that represents a user in the system.

    Attributes:
        sub (str): The subject of the user, a unique identifier Example: mhuttner.
        scopes (List[str]): The scopes the user has Example: ['dabih:api'].
        is_admin (bool): Does the user have the dabih:admin scope
    """

    sub: str
    scopes: List[str]
    is_admin: bool

    def to_dict(self) -> Dict[str, Any]:
        sub = self.sub

        scopes = self.scopes

        is_admin = self.is_admin

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sub": sub,
                "scopes": scopes,
                "isAdmin": is_admin,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sub = d.pop("sub")

        scopes = cast(List[str], d.pop("scopes"))

        is_admin = d.pop("isAdmin")

        user = cls(
            sub=sub,
            scopes=scopes,
            is_admin=is_admin,
        )

        return user
