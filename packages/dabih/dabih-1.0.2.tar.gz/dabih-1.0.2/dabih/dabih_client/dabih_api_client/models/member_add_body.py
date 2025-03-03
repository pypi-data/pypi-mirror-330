from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.file_decryption_key import FileDecryptionKey


T = TypeVar("T", bound="MemberAddBody")


@_attrs_define
class MemberAddBody:
    """
    Attributes:
        subs (List[str]): The users to add to the dataset
        keys (List['FileDecryptionKey']): The list of AES-256 keys required to decrypt all child datasets
    """

    subs: List[str]
    keys: List["FileDecryptionKey"]

    def to_dict(self) -> Dict[str, Any]:
        subs = self.subs

        keys = []
        for keys_item_data in self.keys:
            keys_item = keys_item_data.to_dict()
            keys.append(keys_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "subs": subs,
                "keys": keys,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_decryption_key import FileDecryptionKey

        d = src_dict.copy()
        subs = cast(List[str], d.pop("subs"))

        keys = []
        _keys = d.pop("keys")
        for keys_item_data in _keys:
            keys_item = FileDecryptionKey.from_dict(keys_item_data)

            keys.append(keys_item)

        member_add_body = cls(
            subs=subs,
            keys=keys,
        )

        return member_add_body
