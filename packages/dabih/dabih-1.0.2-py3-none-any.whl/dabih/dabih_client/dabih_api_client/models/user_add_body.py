from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.crypto_json_web_key import CryptoJsonWebKey


T = TypeVar("T", bound="UserAddBody")


@_attrs_define
class UserAddBody:
    """
    Attributes:
        name (str): The name of the user
        email (str): The email of the user
        key (CryptoJsonWebKey):
        sub (Union[Unset, str]): The unique user sub
            if undefined the sub from the auth token will be used
        is_root_key (Union[Unset, bool]): If true the key is a root key, used to decrypt all datasets
    """

    name: str
    email: str
    key: "CryptoJsonWebKey"
    sub: Union[Unset, str] = UNSET
    is_root_key: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        email = self.email

        key = self.key.to_dict()

        sub = self.sub

        is_root_key = self.is_root_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "email": email,
                "key": key,
            }
        )
        if sub is not UNSET:
            field_dict["sub"] = sub
        if is_root_key is not UNSET:
            field_dict["isRootKey"] = is_root_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.crypto_json_web_key import CryptoJsonWebKey

        d = src_dict.copy()
        name = d.pop("name")

        email = d.pop("email")

        key = CryptoJsonWebKey.from_dict(d.pop("key"))

        sub = d.pop("sub", UNSET)

        is_root_key = d.pop("isRootKey", UNSET)

        user_add_body = cls(
            name=name,
            email=email,
            key=key,
            sub=sub,
            is_root_key=is_root_key,
        )

        return user_add_body
