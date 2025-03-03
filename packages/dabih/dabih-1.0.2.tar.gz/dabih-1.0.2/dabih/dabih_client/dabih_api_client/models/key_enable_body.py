from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="KeyEnableBody")


@_attrs_define
class KeyEnableBody:
    """
    Attributes:
        sub (str): The user the key belongs to
        hash_ (str): The hash of the key
        enabled (bool): The key status to set
    """

    sub: str
    hash_: str
    enabled: bool

    def to_dict(self) -> Dict[str, Any]:
        sub = self.sub

        hash_ = self.hash_

        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sub": sub,
                "hash": hash_,
                "enabled": enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sub = d.pop("sub")

        hash_ = d.pop("hash")

        enabled = d.pop("enabled")

        key_enable_body = cls(
            sub=sub,
            hash_=hash_,
            enabled=enabled,
        )

        return key_enable_body
