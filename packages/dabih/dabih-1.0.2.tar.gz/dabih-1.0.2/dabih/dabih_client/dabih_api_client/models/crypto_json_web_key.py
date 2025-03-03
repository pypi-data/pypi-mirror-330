from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CryptoJsonWebKey")


@_attrs_define
class CryptoJsonWebKey:
    """
    Attributes:
        crv (Union[Unset, str]):
        d (Union[Unset, str]):
        dp (Union[Unset, str]):
        dq (Union[Unset, str]):
        e (Union[Unset, str]):
        k (Union[Unset, str]):
        kty (Union[Unset, str]):
        n (Union[Unset, str]):
        p (Union[Unset, str]):
        q (Union[Unset, str]):
        qi (Union[Unset, str]):
        x (Union[Unset, str]):
        y (Union[Unset, str]):
    """

    crv: Union[Unset, str] = UNSET
    d: Union[Unset, str] = UNSET
    dp: Union[Unset, str] = UNSET
    dq: Union[Unset, str] = UNSET
    e: Union[Unset, str] = UNSET
    k: Union[Unset, str] = UNSET
    kty: Union[Unset, str] = UNSET
    n: Union[Unset, str] = UNSET
    p: Union[Unset, str] = UNSET
    q: Union[Unset, str] = UNSET
    qi: Union[Unset, str] = UNSET
    x: Union[Unset, str] = UNSET
    y: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        crv = self.crv

        d = self.d

        dp = self.dp

        dq = self.dq

        e = self.e

        k = self.k

        kty = self.kty

        n = self.n

        p = self.p

        q = self.q

        qi = self.qi

        x = self.x

        y = self.y

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if crv is not UNSET:
            field_dict["crv"] = crv
        if d is not UNSET:
            field_dict["d"] = d
        if dp is not UNSET:
            field_dict["dp"] = dp
        if dq is not UNSET:
            field_dict["dq"] = dq
        if e is not UNSET:
            field_dict["e"] = e
        if k is not UNSET:
            field_dict["k"] = k
        if kty is not UNSET:
            field_dict["kty"] = kty
        if n is not UNSET:
            field_dict["n"] = n
        if p is not UNSET:
            field_dict["p"] = p
        if q is not UNSET:
            field_dict["q"] = q
        if qi is not UNSET:
            field_dict["qi"] = qi
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        crv = d.pop("crv", UNSET)

        d = d.pop("d", UNSET)

        dp = d.pop("dp", UNSET)

        dq = d.pop("dq", UNSET)

        e = d.pop("e", UNSET)

        k = d.pop("k", UNSET)

        kty = d.pop("kty", UNSET)

        n = d.pop("n", UNSET)

        p = d.pop("p", UNSET)

        q = d.pop("q", UNSET)

        qi = d.pop("qi", UNSET)

        x = d.pop("x", UNSET)

        y = d.pop("y", UNSET)

        crypto_json_web_key = cls(
            crv=crv,
            d=d,
            dp=dp,
            dq=dq,
            e=e,
            k=k,
            kty=kty,
            n=n,
            p=p,
            q=q,
            qi=qi,
            x=x,
            y=y,
        )

        crypto_json_web_key.additional_properties = d
        return crypto_json_web_key

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
