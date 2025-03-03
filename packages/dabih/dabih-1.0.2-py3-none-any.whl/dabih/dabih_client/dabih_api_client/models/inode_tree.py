import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.inode_type import InodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_data import FileData
    from ..models.key import Key
    from ..models.member import Member


T = TypeVar("T", bound="InodeTree")


@_attrs_define
class InodeTree:
    """
    Attributes:
        id (Any): The database id of the inode
        mnemonic (str):
        type (InodeType): InodeType is used to represent the type of an Inode.
            FILE: a file
            DIRECTORY: a directory
            UPLOAD: a file that is being uploaded
            TRASH: the special directory that holds deleted files
            ROOT: the global root directory
            HOME: the user's home directory
            USERS: the directory that holds all user directories
        name (str):
        tag (Union[None, str]):
        parent_id (Any):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        members (List['Member']):
        keys (List['Key']):
        data (Union['FileData', None, Unset]):
        children (Union[Unset, List['InodeTree']]):
    """

    id: Any
    mnemonic: str
    type: InodeType
    name: str
    tag: Union[None, str]
    parent_id: Any
    created_at: datetime.datetime
    updated_at: datetime.datetime
    members: List["Member"]
    keys: List["Key"]
    data: Union["FileData", None, Unset] = UNSET
    children: Union[Unset, List["InodeTree"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.file_data import FileData

        id = self.id

        mnemonic = self.mnemonic

        type = self.type.value

        name = self.name

        tag: Union[None, str]
        tag = self.tag

        parent_id = self.parent_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        members = []
        for members_item_data in self.members:
            members_item = members_item_data.to_dict()
            members.append(members_item)

        keys = []
        for keys_item_data in self.keys:
            keys_item = keys_item_data.to_dict()
            keys.append(keys_item)

        data: Union[Dict[str, Any], None, Unset]
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, FileData):
            data = self.data.to_dict()
        else:
            data = self.data

        children: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "mnemonic": mnemonic,
                "type": type,
                "name": name,
                "tag": tag,
                "parentId": parent_id,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "members": members,
                "keys": keys,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_data import FileData
        from ..models.key import Key
        from ..models.member import Member

        d = src_dict.copy()
        id = d.pop("id")

        mnemonic = d.pop("mnemonic")

        type = InodeType(d.pop("type"))

        name = d.pop("name")

        def _parse_tag(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        tag = _parse_tag(d.pop("tag"))

        parent_id = d.pop("parentId")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        members = []
        _members = d.pop("members")
        for members_item_data in _members:
            members_item = Member.from_dict(members_item_data)

            members.append(members_item)

        keys = []
        _keys = d.pop("keys")
        for keys_item_data in _keys:
            keys_item = Key.from_dict(keys_item_data)

            keys.append(keys_item)

        def _parse_data(data: object) -> Union["FileData", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_1 = FileData.from_dict(data)

                return data_type_1
            except:  # noqa: E722
                pass
            return cast(Union["FileData", None, Unset], data)

        data = _parse_data(d.pop("data", UNSET))

        children = []
        _children = d.pop("children", UNSET)
        for children_item_data in _children or []:
            children_item = InodeTree.from_dict(children_item_data)

            children.append(children_item)

        inode_tree = cls(
            id=id,
            mnemonic=mnemonic,
            type=type,
            name=name,
            tag=tag,
            parent_id=parent_id,
            created_at=created_at,
            updated_at=updated_at,
            members=members,
            keys=keys,
            data=data,
            children=children,
        )

        inode_tree.additional_properties = d
        return inode_tree

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
