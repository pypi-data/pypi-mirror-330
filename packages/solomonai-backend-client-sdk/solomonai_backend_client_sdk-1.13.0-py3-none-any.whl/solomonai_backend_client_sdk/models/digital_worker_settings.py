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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class DigitalWorkerSettings(BaseModel):
    """
    Represents the settings and configurations for a digital worker in the system.
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Unique identifier for the digital worker's settings.")
    worker_name: Optional[StrictStr] = Field(default=None, description="Name of the digital worker.", alias="workerName")
    worker_version: Optional[StrictStr] = Field(default=None, description="Version of the digital worker, allowing different versions to have distinct configurations.", alias="workerVersion")
    enable_logging: Optional[StrictBool] = Field(default=None, description="Indicates whether logging is enabled for this digital worker.", alias="enableLogging")
    __properties: ClassVar[List[str]] = ["id", "workerName", "workerVersion", "enableLogging"]

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
        """Create an instance of DigitalWorkerSettings from a JSON string"""
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
        """Create an instance of DigitalWorkerSettings from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "workerName": obj.get("workerName"),
            "workerVersion": obj.get("workerVersion"),
            "enableLogging": obj.get("enableLogging")
        })
        return _obj


