from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_decryption_key import FileDecryptionKey


T = TypeVar("T", bound="MoveInodeBody")


@_attrs_define
class MoveInodeBody:
    """
    Attributes:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        parent (Union[None, Unset, str]): Optional: The mnemonic of the new parent directory
        keys (Union[Unset, List['FileDecryptionKey']]): The list of AES-256 keys required to decrypt all child datasets
        name (Union[Unset, str]): Optional: The new name of the inode
        tag (Union[Unset, str]): Optional: The new tag of the inode
    """

    mnemonic: str
    parent: Union[None, Unset, str] = UNSET
    keys: Union[Unset, List["FileDecryptionKey"]] = UNSET
    name: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        mnemonic = self.mnemonic

        parent: Union[None, Unset, str]
        if isinstance(self.parent, Unset):
            parent = UNSET
        else:
            parent = self.parent

        keys: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.keys, Unset):
            keys = []
            for keys_item_data in self.keys:
                keys_item = keys_item_data.to_dict()
                keys.append(keys_item)

        name = self.name

        tag = self.tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "mnemonic": mnemonic,
            }
        )
        if parent is not UNSET:
            field_dict["parent"] = parent
        if keys is not UNSET:
            field_dict["keys"] = keys
        if name is not UNSET:
            field_dict["name"] = name
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_decryption_key import FileDecryptionKey

        d = src_dict.copy()
        mnemonic = d.pop("mnemonic")

        def _parse_parent(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent = _parse_parent(d.pop("parent", UNSET))

        keys = []
        _keys = d.pop("keys", UNSET)
        for keys_item_data in _keys or []:
            keys_item = FileDecryptionKey.from_dict(keys_item_data)

            keys.append(keys_item)

        name = d.pop("name", UNSET)

        tag = d.pop("tag", UNSET)

        move_inode_body = cls(
            mnemonic=mnemonic,
            parent=parent,
            keys=keys,
            name=name,
            tag=tag,
        )

        return move_inode_body
