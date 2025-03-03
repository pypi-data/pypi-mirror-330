import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="Token")


@_attrs_define
class Token:
    """
    Attributes:
        id (Any): The id of the token
        value (str):
        sub (str):
        scope (str):
        exp (Union[None, datetime.datetime]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: Any
    value: str
    sub: str
    scope: str
    exp: Union[None, datetime.datetime]
    created_at: datetime.datetime
    updated_at: datetime.datetime

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "value": value,
                "sub": sub,
                "scope": scope,
                "exp": exp,
                "createdAt": created_at,
                "updatedAt": updated_at,
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

        token = cls(
            id=id,
            value=value,
            sub=sub,
            scope=scope,
            exp=exp,
            created_at=created_at,
            updated_at=updated_at,
        )

        return token
