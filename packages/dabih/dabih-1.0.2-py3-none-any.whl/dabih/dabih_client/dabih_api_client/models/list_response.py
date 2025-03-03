from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.inode_members import InodeMembers


T = TypeVar("T", bound="ListResponse")


@_attrs_define
class ListResponse:
    """
    Attributes:
        parents (List['InodeMembers']): The list of parent directories
        children (List['InodeMembers']): The list of inodes in the directory
    """

    parents: List["InodeMembers"]
    children: List["InodeMembers"]

    def to_dict(self) -> Dict[str, Any]:
        parents = []
        for parents_item_data in self.parents:
            parents_item = parents_item_data.to_dict()
            parents.append(parents_item)

        children = []
        for children_item_data in self.children:
            children_item = children_item_data.to_dict()
            children.append(children_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "parents": parents,
                "children": children,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.inode_members import InodeMembers

        d = src_dict.copy()
        parents = []
        _parents = d.pop("parents")
        for parents_item_data in _parents:
            parents_item = InodeMembers.from_dict(parents_item_data)

            parents.append(parents_item)

        children = []
        _children = d.pop("children")
        for children_item_data in _children:
            children_item = InodeMembers.from_dict(children_item_data)

            children.append(children_item)

        list_response = cls(
            parents=parents,
            children=children,
        )

        return list_response
