import datetime
from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="Directory")


@_attrs_define
class Directory:
    """
    Attributes:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        name (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    mnemonic: str
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        mnemonic = self.mnemonic

        name = self.name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "mnemonic": mnemonic,
                "name": name,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mnemonic = d.pop("mnemonic")

        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        directory = cls(
            mnemonic=mnemonic,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
        )

        return directory
