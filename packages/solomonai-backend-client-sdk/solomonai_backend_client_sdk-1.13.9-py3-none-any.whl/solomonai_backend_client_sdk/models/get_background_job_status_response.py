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
from solomonai_backend_client_sdk.models.background_job_status import BackgroundJobStatus
from typing import Optional, Set
from typing_extensions import Self

class GetBackgroundJobStatusResponse(BaseModel):
    """
    GetBackgroundJobStatusResponse represents the current status of a background job. Provides information about job progress and estimated completion.  Fields: - status: Current status of the background job - estimated_completion_time: Expected completion timestamp - job_id: The unique identifier of the job being tracked
    """ # noqa: E501
    status: Optional[BackgroundJobStatus] = BackgroundJobStatus.UNSPECIFIED
    estimated_completion_time: Optional[datetime] = Field(default=None, alias="estimatedCompletionTime")
    job_id: StrictStr = Field(alias="jobId")
    __properties: ClassVar[List[str]] = ["status", "estimatedCompletionTime", "jobId"]

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
        """Create an instance of GetBackgroundJobStatusResponse from a JSON string"""
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
        """Create an instance of GetBackgroundJobStatusResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "status": obj.get("status") if obj.get("status") is not None else BackgroundJobStatus.UNSPECIFIED,
            "estimatedCompletionTime": obj.get("estimatedCompletionTime"),
            "jobId": obj.get("jobId")
        })
        return _obj


