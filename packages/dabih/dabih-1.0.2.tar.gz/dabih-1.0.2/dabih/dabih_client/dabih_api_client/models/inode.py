import datetime
from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.inode_type import InodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_data import FileData


T = TypeVar("T", bound="Inode")


@_attrs_define
class Inode:
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
        data (Union['FileData', None, Unset]):
    """

    id: Any
    mnemonic: str
    type: InodeType
    name: str
    tag: Union[None, str]
    parent_id: Any
    created_at: datetime.datetime
    updated_at: datetime.datetime
    data: Union["FileData", None, Unset] = UNSET

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

        data: Union[Dict[str, Any], None, Unset]
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, FileData):
            data = self.data.to_dict()
        else:
            data = self.data

        field_dict: Dict[str, Any] = {}
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
            }
        )
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_data import FileData

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

        inode = cls(
            id=id,
            mnemonic=mnemonic,
            type=type,
            name=name,
            tag=tag,
            parent_id=parent_id,
            created_at=created_at,
            updated_at=updated_at,
            data=data,
        )

        return inode
