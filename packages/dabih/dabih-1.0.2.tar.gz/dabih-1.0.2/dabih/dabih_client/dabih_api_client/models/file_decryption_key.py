from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="FileDecryptionKey")


@_attrs_define
class FileDecryptionKey:
    """
    Attributes:
        mnemonic (str): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        key (str): The AES-256 encryption key used to encrypt and decrypt datasets.
            base64url encoded
    """

    mnemonic: str
    key: str

    def to_dict(self) -> Dict[str, Any]:
        mnemonic = self.mnemonic

        key = self.key

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "mnemonic": mnemonic,
                "key": key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mnemonic = d.pop("mnemonic")

        key = d.pop("key")

        file_decryption_key = cls(
            mnemonic=mnemonic,
            key=key,
        )

        return file_decryption_key
