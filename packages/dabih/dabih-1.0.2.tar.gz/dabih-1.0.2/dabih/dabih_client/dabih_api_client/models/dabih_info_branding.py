from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dabih_info_branding_admin import DabihInfoBrandingAdmin
    from ..models.dabih_info_branding_contact import DabihInfoBrandingContact
    from ..models.dabih_info_branding_department import DabihInfoBrandingDepartment
    from ..models.dabih_info_branding_organization import DabihInfoBrandingOrganization


T = TypeVar("T", bound="DabihInfoBranding")


@_attrs_define
class DabihInfoBranding:
    """
    Attributes:
        organization (DabihInfoBrandingOrganization):
        department (DabihInfoBrandingDepartment):
        contact (DabihInfoBrandingContact):
        admin (DabihInfoBrandingAdmin):
    """

    organization: "DabihInfoBrandingOrganization"
    department: "DabihInfoBrandingDepartment"
    contact: "DabihInfoBrandingContact"
    admin: "DabihInfoBrandingAdmin"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        organization = self.organization.to_dict()

        department = self.department.to_dict()

        contact = self.contact.to_dict()

        admin = self.admin.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization": organization,
                "department": department,
                "contact": contact,
                "admin": admin,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dabih_info_branding_admin import DabihInfoBrandingAdmin
        from ..models.dabih_info_branding_contact import DabihInfoBrandingContact
        from ..models.dabih_info_branding_department import DabihInfoBrandingDepartment
        from ..models.dabih_info_branding_organization import DabihInfoBrandingOrganization

        d = src_dict.copy()
        organization = DabihInfoBrandingOrganization.from_dict(d.pop("organization"))

        department = DabihInfoBrandingDepartment.from_dict(d.pop("department"))

        contact = DabihInfoBrandingContact.from_dict(d.pop("contact"))

        admin = DabihInfoBrandingAdmin.from_dict(d.pop("admin"))

        dabih_info_branding = cls(
            organization=organization,
            department=department,
            contact=contact,
            admin=admin,
        )

        dabih_info_branding.additional_properties = d
        return dabih_info_branding

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
