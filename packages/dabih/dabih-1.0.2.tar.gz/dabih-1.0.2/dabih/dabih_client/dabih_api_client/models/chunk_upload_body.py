from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="ChunkUploadBody")


@_attrs_define
class ChunkUploadBody:
    """
    Attributes:
        chunk (Union[Unset, File]):
    """

    chunk: Union[Unset, File] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chunk: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.chunk, Unset):
            chunk = self.chunk.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if chunk is not UNSET:
            field_dict["chunk"] = chunk

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        chunk: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.chunk, Unset):
            chunk = self.chunk.to_tuple()

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if chunk is not UNSET:
            field_dict["chunk"] = chunk

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _chunk = d.pop("chunk", UNSET)
        chunk: Union[Unset, File]
        if isinstance(_chunk, Unset):
            chunk = UNSET
        else:
            chunk = File(payload=BytesIO(_chunk))

        chunk_upload_body = cls(
            chunk=chunk,
        )

        chunk_upload_body.additional_properties = d
        return chunk_upload_body

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
