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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class EmployeeBenefits(BaseModel):
    """
    The Benefit object is used to represent a benefit that an employee has enrolled in.
    """ # noqa: E501
    id: Optional[StrictStr] = None
    remote_id: Optional[StrictStr] = Field(default=None, description="The third-party API ID of the matching object.", alias="remoteId")
    provider_name: Optional[StrictStr] = Field(default=None, description="The name of the benefit provider.", alias="providerName")
    employee_merge_account_id: Optional[StrictStr] = Field(default=None, description="The ID of the employee.", alias="employeeMergeAccountId")
    benefit_plan_merge_account_id: Optional[StrictStr] = Field(default=None, description="The ID of the benefit plan.", alias="benefitPlanMergeAccountId")
    employee_contribution: Optional[StrictStr] = Field(default=None, description="The employee's contribution.", alias="employeeContribution")
    company_contribution: Optional[StrictStr] = Field(default=None, description="The company's contribution.", alias="companyContribution")
    start_date: Optional[datetime] = Field(default=None, description="The day and time the benefit started.", alias="startDate")
    end_date: Optional[datetime] = Field(default=None, description="The day and time the benefit ended.", alias="endDate")
    remote_was_deleted: Optional[StrictBool] = Field(default=None, description="Indicates whether or not this object has been deleted in the third party platform.", alias="remoteWasDeleted")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    modified_at: Optional[datetime] = Field(default=None, alias="modifiedAt")
    merge_account_id: Optional[StrictStr] = Field(default=None, alias="mergeAccountId")
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    __properties: ClassVar[List[str]] = ["id", "remoteId", "providerName", "employeeMergeAccountId", "benefitPlanMergeAccountId", "employeeContribution", "companyContribution", "startDate", "endDate", "remoteWasDeleted", "createdAt", "modifiedAt", "mergeAccountId", "deletedAt"]

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
        """Create an instance of EmployeeBenefits from a JSON string"""
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
        """Create an instance of EmployeeBenefits from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "remoteId": obj.get("remoteId"),
            "providerName": obj.get("providerName"),
            "employeeMergeAccountId": obj.get("employeeMergeAccountId"),
            "benefitPlanMergeAccountId": obj.get("benefitPlanMergeAccountId"),
            "employeeContribution": obj.get("employeeContribution"),
            "companyContribution": obj.get("companyContribution"),
            "startDate": obj.get("startDate"),
            "endDate": obj.get("endDate"),
            "remoteWasDeleted": obj.get("remoteWasDeleted"),
            "createdAt": obj.get("createdAt"),
            "modifiedAt": obj.get("modifiedAt"),
            "mergeAccountId": obj.get("mergeAccountId"),
            "deletedAt": obj.get("deletedAt")
        })
        return _obj


