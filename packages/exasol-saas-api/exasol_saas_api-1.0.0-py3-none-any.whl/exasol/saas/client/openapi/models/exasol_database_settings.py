from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Optional,
    TextIO,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import (
    UNSET,
    Unset,
)

T = TypeVar("T", bound="ExasolDatabaseSettings")


@_attrs_define
class ExasolDatabaseSettings:
    """ 
        Attributes:
            offload_enabled (bool):
            auto_updates_enabled (bool):
            auto_updates_hard_disabled (bool):
            num_nodes (int):
     """

    offload_enabled: bool
    auto_updates_enabled: bool
    auto_updates_hard_disabled: bool
    num_nodes: int


    def to_dict(self) -> dict[str, Any]:
        offload_enabled = self.offload_enabled

        auto_updates_enabled = self.auto_updates_enabled

        auto_updates_hard_disabled = self.auto_updates_hard_disabled

        num_nodes = self.num_nodes


        field_dict: dict[str, Any] = {}
        field_dict.update({
            "offloadEnabled": offload_enabled,
            "autoUpdatesEnabled": auto_updates_enabled,
            "autoUpdatesHardDisabled": auto_updates_hard_disabled,
            "numNodes": num_nodes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        offload_enabled = d.pop("offloadEnabled")

        auto_updates_enabled = d.pop("autoUpdatesEnabled")

        auto_updates_hard_disabled = d.pop("autoUpdatesHardDisabled")

        num_nodes = d.pop("numNodes")

        exasol_database_settings = cls(
            offload_enabled=offload_enabled,
            auto_updates_enabled=auto_updates_enabled,
            auto_updates_hard_disabled=auto_updates_hard_disabled,
            num_nodes=num_nodes,
        )

        return exasol_database_settings

