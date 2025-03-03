from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.crypto_json_web_key import CryptoJsonWebKey


T = TypeVar("T", bound="KeyAddBody")


@_attrs_define
class KeyAddBody:
    """
    Attributes:
        sub (str): The user the key should belong to
        data (CryptoJsonWebKey):
        is_root_key (bool): If true the key is a root key, used to decrypt all datasets
    """

    sub: str
    data: "CryptoJsonWebKey"
    is_root_key: bool

    def to_dict(self) -> Dict[str, Any]:
        sub = self.sub

        data = self.data.to_dict()

        is_root_key = self.is_root_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sub": sub,
                "data": data,
                "isRootKey": is_root_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.crypto_json_web_key import CryptoJsonWebKey

        d = src_dict.copy()
        sub = d.pop("sub")

        data = CryptoJsonWebKey.from_dict(d.pop("data"))

        is_root_key = d.pop("isRootKey")

        key_add_body = cls(
            sub=sub,
            data=data,
            is_root_key=is_root_key,
        )

        return key_add_body
