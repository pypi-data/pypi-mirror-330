from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadStartBody")


@_attrs_define
class UploadStartBody:
    """
    Attributes:
        file_name (str): The name of the file to upload
        directory (Union[Unset, str]): mnemonics are human readable unique identifiers for datasets
            mnemonics have the form <random adjective>_<random first name> Example: happy_jane.
        file_path (Union[Unset, str]): The original path of the file
        size (Union[Unset, int]): The size of the file in bytes
        tag (Union[Unset, str]): A custom searchable tag for the file
    """

    file_name: str
    directory: Union[Unset, str] = UNSET
    file_path: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    tag: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        file_name = self.file_name

        directory = self.directory

        file_path = self.file_path

        size = self.size

        tag = self.tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fileName": file_name,
            }
        )
        if directory is not UNSET:
            field_dict["directory"] = directory
        if file_path is not UNSET:
            field_dict["filePath"] = file_path
        if size is not UNSET:
            field_dict["size"] = size
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_name = d.pop("fileName")

        directory = d.pop("directory", UNSET)

        file_path = d.pop("filePath", UNSET)

        size = d.pop("size", UNSET)

        tag = d.pop("tag", UNSET)

        upload_start_body = cls(
            file_name=file_name,
            directory=directory,
            file_path=file_path,
            size=size,
            tag=tag,
        )

        return upload_start_body
