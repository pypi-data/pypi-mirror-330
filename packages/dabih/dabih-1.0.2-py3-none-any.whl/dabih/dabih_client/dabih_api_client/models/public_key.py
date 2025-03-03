import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="PublicKey")


@_attrs_define
class PublicKey:
    """
    Attributes:
        id (Any): The database id of the public key
        user_id (Any): The user id the key belongs to
        hash_ (str):
        data (str):
        is_root_key (bool):
        enabled (Union[None, datetime.datetime]):
        enabled_by (Union[None, str]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: Any
    user_id: Any
    hash_: str
    data: str
    is_root_key: bool
    enabled: Union[None, datetime.datetime]
    enabled_by: Union[None, str]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        user_id = self.user_id

        hash_ = self.hash_

        data = self.data

        is_root_key = self.is_root_key

        enabled: Union[None, str]
        if isinstance(self.enabled, datetime.datetime):
            enabled = self.enabled.isoformat()
        else:
            enabled = self.enabled

        enabled_by: Union[None, str]
        enabled_by = self.enabled_by

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "userId": user_id,
                "hash": hash_,
                "data": data,
                "isRootKey": is_root_key,
                "enabled": enabled,
                "enabledBy": enabled_by,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        user_id = d.pop("userId")

        hash_ = d.pop("hash")

        data = d.pop("data")

        is_root_key = d.pop("isRootKey")

        def _parse_enabled(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                enabled_type_0 = isoparse(data)

                return enabled_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        enabled = _parse_enabled(d.pop("enabled"))

        def _parse_enabled_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        enabled_by = _parse_enabled_by(d.pop("enabledBy"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        public_key = cls(
            id=id,
            user_id=user_id,
            hash_=hash_,
            data=data,
            is_root_key=is_root_key,
            enabled=enabled,
            enabled_by=enabled_by,
            created_at=created_at,
            updated_at=updated_at,
        )

        return public_key
