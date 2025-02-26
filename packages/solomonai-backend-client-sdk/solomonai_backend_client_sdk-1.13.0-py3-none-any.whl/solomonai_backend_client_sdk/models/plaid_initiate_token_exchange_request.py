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
from solomonai_backend_client_sdk.models.financial_user_profile_type import FinancialUserProfileType
from typing import Optional, Set
from typing_extensions import Self

class PlaidInitiateTokenExchangeRequest(BaseModel):
    """
    PlaidInitiateTokenExchangeRequest
    """ # noqa: E501
    user_id: StrictStr = Field(alias="userId")
    full_name: StrictStr = Field(description="The user's full legal name. This is an optional field used in the [returning user experience](https://plaid.com/docs/link/returning-user) to associate Items to the user.", alias="fullName")
    email: StrictStr = Field(description="The user's email address. This field is optional, but required to enable the [pre-authenticated returning user flow](https://plaid.com/docs/link/returning-user/#enabling-the-returning-user-experience).")
    phone_number: StrictStr = Field(description="The user's phone number in [E.164](https://en.wikipedia.org/wiki/E.164) format. This field is optional, but required to enable the [returning user experience](https://plaid.com/docs/link/returning-user).", alias="phoneNumber")
    profile_type: FinancialUserProfileType = Field(alias="profileType")
    org_id: StrictStr = Field(description="Organization identifier for multi-org support", alias="orgId")
    tenant_id: StrictStr = Field(description="Tenant identifier for multi-tenancy support", alias="tenantId")
    __properties: ClassVar[List[str]] = ["userId", "fullName", "email", "phoneNumber", "profileType", "orgId", "tenantId"]

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
        """Create an instance of PlaidInitiateTokenExchangeRequest from a JSON string"""
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
        """Create an instance of PlaidInitiateTokenExchangeRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "userId": obj.get("userId"),
            "fullName": obj.get("fullName"),
            "email": obj.get("email"),
            "phoneNumber": obj.get("phoneNumber"),
            "profileType": obj.get("profileType") if obj.get("profileType") is not None else FinancialUserProfileType.UNSPECIFIED,
            "orgId": obj.get("orgId"),
            "tenantId": obj.get("tenantId")
        })
        return _obj


