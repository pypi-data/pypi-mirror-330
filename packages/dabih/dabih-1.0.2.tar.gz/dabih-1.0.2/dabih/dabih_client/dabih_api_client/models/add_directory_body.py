from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddDirectoryBody")


@_attrs_define
class AddDirectoryBody:
    """
    Attributes:
        name (str): The name of the directory
        parent (Union[Unset, str]): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        tag (Union[Unset, str]): A custom searchable tag for the directory
    """

    name: str
    parent: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        parent = self.parent

        tag = self.tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if parent is not UNSET:
            field_dict["parent"] = parent
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        parent = d.pop("parent", UNSET)

        tag = d.pop("tag", UNSET)

        add_directory_body = cls(
            name=name,
            parent=parent,
            tag=tag,
        )

        return add_directory_body
