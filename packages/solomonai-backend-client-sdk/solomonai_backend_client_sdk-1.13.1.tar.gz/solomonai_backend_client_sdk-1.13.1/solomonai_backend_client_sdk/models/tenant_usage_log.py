# coding: utf-8

"""
    User Service API

    Solomon AI User Service API - Manages user profiles and authentication

    The version of the OpenAPI document: 1.0
    Contact: yoanyomba@solomon-ai.co
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from solomonai_backend_client_sdk.models.event_type import EventType
from solomonai_backend_client_sdk.models.storage_unit import StorageUnit
from typing import Optional, Set
from typing_extensions import Self

class TenantUsageLog(BaseModel):
    """
    TenantUsageLog
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Unique identifier for the usage log.")
    timestamp: Optional[datetime] = Field(default=None, description="Timestamp of the log entry.")
    event_type: Optional[EventType] = Field(default=EventType.UNSPECIFIED, alias="eventType")
    quantity: Optional[StrictStr] = Field(default=None, description="Quantity of the resource used.")
    unit: Optional[StorageUnit] = StorageUnit.UNSPECIFIED
    details: Optional[StrictStr] = Field(default=None, description="Details in JSON format.")
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    __properties: ClassVar[List[str]] = ["id", "timestamp", "eventType", "quantity", "unit", "details", "deletedAt"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of TenantUsageLog from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TenantUsageLog from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "timestamp": obj.get("timestamp"),
            "eventType": obj.get("eventType") if obj.get("eventType") is not None else EventType.UNSPECIFIED,
            "quantity": obj.get("quantity"),
            "unit": obj.get("unit") if obj.get("unit") is not None else StorageUnit.UNSPECIFIED,
            "details": obj.get("details"),
            "deletedAt": obj.get("deletedAt")
        })
        return _obj


