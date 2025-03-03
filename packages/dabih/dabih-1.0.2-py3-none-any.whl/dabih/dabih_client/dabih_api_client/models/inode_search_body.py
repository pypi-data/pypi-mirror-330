from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="InodeSearchBody")


@_attrs_define
class InodeSearchBody:
    """
    Attributes:
        query (str):
    """

    query: str

    def to_dict(self) -> Dict[str, Any]:
        query = self.query

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "query": query,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query = d.pop("query")

        inode_search_body = cls(
            query=query,
        )

        return inode_search_body
