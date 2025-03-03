from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.dabih_info_branding import DabihInfoBranding


T = TypeVar("T", bound="DabihInfo")


@_attrs_define
class DabihInfo:
    """
    Attributes:
        version (str):
        branding (DabihInfoBranding):
    """

    version: str
    branding: "DabihInfoBranding"

    def to_dict(self) -> Dict[str, Any]:
        version = self.version

        branding = self.branding.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "version": version,
                "branding": branding,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dabih_info_branding import DabihInfoBranding

        d = src_dict.copy()
        version = d.pop("version")

        branding = DabihInfoBranding.from_dict(d.pop("branding"))

        dabih_info = cls(
            version=version,
            branding=branding,
        )

        return dabih_info
