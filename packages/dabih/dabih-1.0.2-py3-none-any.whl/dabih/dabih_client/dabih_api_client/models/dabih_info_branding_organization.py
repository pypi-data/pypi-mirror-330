from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DabihInfoBrandingOrganization")


@_attrs_define
class DabihInfoBrandingOrganization:
    """
    Attributes:
        logo (str):
        url (str):
        name (str):
    """

    logo: str
    url: str
    name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        logo = self.logo

        url = self.url

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "logo": logo,
                "url": url,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        logo = d.pop("logo")

        url = d.pop("url")

        name = d.pop("name")

        dabih_info_branding_organization = cls(
            logo=logo,
            url=url,
            name=name,
        )

        dabih_info_branding_organization.additional_properties = d
        return dabih_info_branding_organization

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
