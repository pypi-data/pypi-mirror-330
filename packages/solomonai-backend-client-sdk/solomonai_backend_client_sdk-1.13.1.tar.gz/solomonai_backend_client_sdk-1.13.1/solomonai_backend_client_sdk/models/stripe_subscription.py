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
from solomonai_backend_client_sdk.models.stripe_subscription_status import StripeSubscriptionStatus
from typing import Optional, Set
from typing_extensions import Self

class StripeSubscription(BaseModel):
    """
    StripeSubscription
    """ # noqa: E501
    id: Optional[StrictStr] = None
    stripe_subscription_id: Optional[StrictStr] = Field(default=None, alias="stripeSubscriptionId")
    stripe_subscription_status: Optional[StripeSubscriptionStatus] = Field(default=StripeSubscriptionStatus.UNSPECIFIED, alias="stripeSubscriptionStatus")
    stripe_subscription_active_until: Optional[StrictStr] = Field(default=None, alias="stripeSubscriptionActiveUntil")
    stripe_webhook_latest_timestamp: Optional[StrictStr] = Field(default=None, alias="stripeWebhookLatestTimestamp")
    is_trialing: Optional[StrictBool] = Field(default=None, alias="isTrialing")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    __properties: ClassVar[List[str]] = ["id", "stripeSubscriptionId", "stripeSubscriptionStatus", "stripeSubscriptionActiveUntil", "stripeWebhookLatestTimestamp", "isTrialing", "createdAt", "deletedAt"]

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
        """Create an instance of StripeSubscription from a JSON string"""
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
        """Create an instance of StripeSubscription from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "stripeSubscriptionId": obj.get("stripeSubscriptionId"),
            "stripeSubscriptionStatus": obj.get("stripeSubscriptionStatus") if obj.get("stripeSubscriptionStatus") is not None else StripeSubscriptionStatus.UNSPECIFIED,
            "stripeSubscriptionActiveUntil": obj.get("stripeSubscriptionActiveUntil"),
            "stripeWebhookLatestTimestamp": obj.get("stripeWebhookLatestTimestamp"),
            "isTrialing": obj.get("isTrialing"),
            "createdAt": obj.get("createdAt"),
            "deletedAt": obj.get("deletedAt")
        })
        return _obj


