"""InvenioRDM API models"""

from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict


class Access(str, Enum):
    """
    * PUBLIC: Indicates that a record or file is visible to anyone.
    * RESTRICTED: Indicates that a record or file is only visible
        to the owner or certain users.
    """

    PUBLIC = "public"
    RESTRICTED = "restricted"


class DraftConfig(BaseModel):
    """
    The configuration options for creating a draft record.

    Attributes:
        record_access (Access): Access option for the record.
        files_access (Access): Access option for the record files.
        files_enabled (bool): Indicates whether files can attached to this record.
        metadata (Dict[str, Any]): Metadata of the record.
        default_preview (Optional[str]): Name of the file to be previewed by default.
        order (Optional[List[str]]): Array of file names in display order.
        community_id: (Optional[str]): The ID of the community to associate with the record.
        custom_fields (Optional[Dict[str, Any]]): Custom fields.
    """

    model_config = ConfigDict(use_enum_values=True)

    record_access: Access
    files_access: Access
    files_enabled: bool
    metadata: Dict[str, Any]
    default_preview: Optional[str] = None
    order: Optional[List[str]] = None
    community_id: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    pids: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the model to a dictionary.
        """
        json = {
            "access": {
                "record": self.record_access,
                "files": self.files_access,
            },
            "files": {"enabled": self.files_enabled},
            "metadata": self.metadata,
        }

        if self.default_preview:
            json["default_preview"] = self.default_preview

        if self.order:
            json["order"] = self.order

        if self.custom_fields:
            json["custom_fields"] = self.custom_fields

        if self.pids:
            json["pids"] = self.pids

        return json
