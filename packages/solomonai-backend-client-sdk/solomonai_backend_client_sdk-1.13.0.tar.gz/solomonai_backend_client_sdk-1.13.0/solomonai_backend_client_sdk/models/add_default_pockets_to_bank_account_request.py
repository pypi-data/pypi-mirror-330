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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from solomonai_backend_client_sdk.models.financial_account_type import FinancialAccountType
from solomonai_backend_client_sdk.models.financial_user_profile_type import FinancialUserProfileType
from typing import Optional, Set
from typing_extensions import Self

class AddDefaultPocketsToBankAccountRequest(BaseModel):
    """
    AddDefaultPocketsToBankAccountRequest
    """ # noqa: E501
    user_id: StrictStr = Field(alias="userId")
    plaid_account_id: StrictStr = Field(alias="plaidAccountId")
    profile_type: FinancialUserProfileType = Field(alias="profileType")
    financial_account_type: FinancialAccountType = Field(alias="financialAccountType")
    org_id: StrictStr = Field(description="Organization identifier for multi-org support", alias="orgId")
    tenant_id: StrictStr = Field(description="Tenant identifier for multi-tenancy support", alias="tenantId")
    __properties: ClassVar[List[str]] = ["userId", "plaidAccountId", "profileType", "financialAccountType", "orgId", "tenantId"]

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
        """Create an instance of AddDefaultPocketsToBankAccountRequest from a JSON string"""
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
        """Create an instance of AddDefaultPocketsToBankAccountRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "userId": obj.get("userId"),
            "plaidAccountId": obj.get("plaidAccountId"),
            "profileType": obj.get("profileType") if obj.get("profileType") is not None else FinancialUserProfileType.UNSPECIFIED,
            "financialAccountType": obj.get("financialAccountType") if obj.get("financialAccountType") is not None else FinancialAccountType.UNSPECIFIED,
            "orgId": obj.get("orgId"),
            "tenantId": obj.get("tenantId")
        })
        return _obj


