from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="KeyRemoveBody")


@_attrs_define
class KeyRemoveBody:
    """
    Attributes:
        sub (str): The user the key belongs to
        hash_ (str): The hash of the key
    """

    sub: str
    hash_: str

    def to_dict(self) -> Dict[str, Any]:
        sub = self.sub

        hash_ = self.hash_

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sub": sub,
                "hash": hash_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sub = d.pop("sub")

        hash_ = d.pop("hash")

        key_remove_body = cls(
            sub=sub,
            hash_=hash_,
        )

        return key_remove_body
