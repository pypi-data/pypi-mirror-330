import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.chunk import Chunk


T = TypeVar("T", bound="ChunkData")


@_attrs_define
class ChunkData:
    """
    Attributes:
        id (Any): The database id of the file data
        uid (str):
        created_by (str):
        file_name (str):
        file_path (Union[None, str]):
        hash_ (Union[None, str]):
        size (Any): The size of the file in bytes
        key_hash (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        chunks (List['Chunk']):
    """

    id: Any
    uid: str
    created_by: str
    file_name: str
    file_path: Union[None, str]
    hash_: Union[None, str]
    size: Any
    key_hash: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    chunks: List["Chunk"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        uid = self.uid

        created_by = self.created_by

        file_name = self.file_name

        file_path: Union[None, str]
        file_path = self.file_path

        hash_: Union[None, str]
        hash_ = self.hash_

        size = self.size

        key_hash = self.key_hash

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        chunks = []
        for chunks_item_data in self.chunks:
            chunks_item = chunks_item_data.to_dict()
            chunks.append(chunks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uid": uid,
                "createdBy": created_by,
                "fileName": file_name,
                "filePath": file_path,
                "hash": hash_,
                "size": size,
                "keyHash": key_hash,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "chunks": chunks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chunk import Chunk

        d = src_dict.copy()
        id = d.pop("id")

        uid = d.pop("uid")

        created_by = d.pop("createdBy")

        file_name = d.pop("fileName")

        def _parse_file_path(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        file_path = _parse_file_path(d.pop("filePath"))

        def _parse_hash_(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        hash_ = _parse_hash_(d.pop("hash"))

        size = d.pop("size")

        key_hash = d.pop("keyHash")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        chunks = []
        _chunks = d.pop("chunks")
        for chunks_item_data in _chunks:
            chunks_item = Chunk.from_dict(chunks_item_data)

            chunks.append(chunks_item)

        chunk_data = cls(
            id=id,
            uid=uid,
            created_by=created_by,
            file_name=file_name,
            file_path=file_path,
            hash_=hash_,
            size=size,
            key_hash=key_hash,
            created_at=created_at,
            updated_at=updated_at,
            chunks=chunks,
        )

        chunk_data.additional_properties = d
        return chunk_data

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
