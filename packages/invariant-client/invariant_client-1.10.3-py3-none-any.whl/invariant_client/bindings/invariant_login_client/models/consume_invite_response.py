from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict

if TYPE_CHECKING:
    from ..models.user_summary import UserSummary


T = TypeVar("T", bound="ConsumeInviteResponse")


@_attrs_define
class ConsumeInviteResponse:
    """
    Attributes:
        user (UserSummary):
    """

    user: "UserSummary"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user = self.user.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_summary import UserSummary

        d = src_dict.copy()
        user = UserSummary.from_dict(d.pop("user"))

        consume_invite_response = cls(
            user=user,
        )

        consume_invite_response.additional_properties = d
        return consume_invite_response

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
