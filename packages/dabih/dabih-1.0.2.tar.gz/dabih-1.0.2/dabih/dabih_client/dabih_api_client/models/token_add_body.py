from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="TokenAddBody")


@_attrs_define
class TokenAddBody:
    """
    Attributes:
        scopes (List[str]): The array of scopes the token should have
        lifetime (Union[None, int]): The time in seconds the token should be valid for
            If null the token will never expire
    """

    scopes: List[str]
    lifetime: Union[None, int]

    def to_dict(self) -> Dict[str, Any]:
        scopes = self.scopes

        lifetime: Union[None, int]
        lifetime = self.lifetime

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "scopes": scopes,
                "lifetime": lifetime,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scopes = cast(List[str], d.pop("scopes"))

        def _parse_lifetime(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        lifetime = _parse_lifetime(d.pop("lifetime"))

        token_add_body = cls(
            scopes=scopes,
            lifetime=lifetime,
        )

        return token_add_body
