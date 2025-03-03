from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.inode import Inode


T = TypeVar("T", bound="InodeSearchResults")


@_attrs_define
class InodeSearchResults:
    """
    Attributes:
        is_complete (bool):
        inodes (List['Inode']): The list of inodes that match the search query
    """

    is_complete: bool
    inodes: List["Inode"]

    def to_dict(self) -> Dict[str, Any]:
        is_complete = self.is_complete

        inodes = []
        for inodes_item_data in self.inodes:
            inodes_item = inodes_item_data.to_dict()
            inodes.append(inodes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "isComplete": is_complete,
                "inodes": inodes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.inode import Inode

        d = src_dict.copy()
        is_complete = d.pop("isComplete")

        inodes = []
        _inodes = d.pop("inodes")
        for inodes_item_data in _inodes:
            inodes_item = Inode.from_dict(inodes_item_data)

            inodes.append(inodes_item)

        inode_search_results = cls(
            is_complete=is_complete,
            inodes=inodes,
        )

        return inode_search_results
