from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DabihInfoBrandingContact")


@_attrs_define
class DabihInfoBrandingContact:
    """
    Attributes:
        phone (str):
        country (str):
        state (str):
        city (str):
        zip_ (str):
        street (str):
        email (str):
        name (str):
    """

    phone: str
    country: str
    state: str
    city: str
    zip_: str
    street: str
    email: str
    name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        phone = self.phone

        country = self.country

        state = self.state

        city = self.city

        zip_ = self.zip_

        street = self.street

        email = self.email

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "phone": phone,
                "country": country,
                "state": state,
                "city": city,
                "zip": zip_,
                "street": street,
                "email": email,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        phone = d.pop("phone")

        country = d.pop("country")

        state = d.pop("state")

        city = d.pop("city")

        zip_ = d.pop("zip")

        street = d.pop("street")

        email = d.pop("email")

        name = d.pop("name")

        dabih_info_branding_contact = cls(
            phone=phone,
            country=country,
            state=state,
            city=city,
            zip_=zip_,
            street=street,
            email=email,
            name=name,
        )

        dabih_info_branding_contact.additional_properties = d
        return dabih_info_branding_contact

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
