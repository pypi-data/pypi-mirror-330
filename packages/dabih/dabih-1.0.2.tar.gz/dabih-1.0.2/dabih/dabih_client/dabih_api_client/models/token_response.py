import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="TokenResponse")


@_attrs_define
class TokenResponse:
    """
    Attributes:
        id (Any): The id of the token
        value (str):
        sub (str):
        scope (str):
        exp (Union[None, datetime.datetime]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        expired (Union[bool, str]): false if the token has not expired,
            otherwise a string describing how long ago the token expired
        scopes (List[str]): The array of scopes the token has
    """

    id: Any
    value: str
    sub: str
    scope: str
    exp: Union[None, datetime.datetime]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    expired: Union[bool, str]
    scopes: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        value = self.value

        sub = self.sub

        scope = self.scope

        exp: Union[None, str]
        if isinstance(self.exp, datetime.datetime):
            exp = self.exp.isoformat()
        else:
            exp = self.exp

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        expired: Union[bool, str]
        expired = self.expired

        scopes = self.scopes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
                "sub": sub,
                "scope": scope,
                "exp": exp,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "expired": expired,
                "scopes": scopes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        value = d.pop("value")

        sub = d.pop("sub")

        scope = d.pop("scope")

        def _parse_exp(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                exp_type_0 = isoparse(data)

                return exp_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        exp = _parse_exp(d.pop("exp"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        def _parse_expired(data: object) -> Union[bool, str]:
            return cast(Union[bool, str], data)

        expired = _parse_expired(d.pop("expired"))

        scopes = cast(List[str], d.pop("scopes"))

        token_response = cls(
            id=id,
            value=value,
            sub=sub,
            scope=scope,
            exp=exp,
            created_at=created_at,
            updated_at=updated_at,
            expired=expired,
            scopes=scopes,
        )

        token_response.additional_properties = d
        return token_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
