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
from solomonai_backend_client_sdk.models.forecast import Forecast
from solomonai_backend_client_sdk.models.goal_type import GoalType
from solomonai_backend_client_sdk.models.milestone import Milestone
from solomonai_backend_client_sdk.models.smart_note import SmartNote
from typing import Optional, Set
from typing_extensions import Self

class SmartGoal(BaseModel):
    """
    SmartGoal: The Goals table stores information about each financial goal, including the name of the goal, its description, the target amount of money the user wants to save or invest, and the expected date of completion.  The Goals table also includes columns for the start date of the goal, the current amount of money saved or invested towards the goal, and a boolean flag indicating whether the goal has been achieved. These additional columns allow the user to track their progress towards the goal and see how much more they need to save or invest to reach their target amount.
    """ # noqa: E501
    id: Optional[StrictStr] = None
    user_id: Optional[StrictStr] = Field(default=None, alias="userId")
    name: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    is_completed: Optional[StrictBool] = Field(default=None, alias="isCompleted")
    goal_type: Optional[GoalType] = Field(default=GoalType.UNSPECIFIED, alias="goalType")
    duration: Optional[StrictStr] = None
    start_date: Optional[StrictStr] = Field(default=None, alias="startDate")
    end_date: Optional[StrictStr] = Field(default=None, alias="endDate")
    target_amount: Optional[StrictStr] = Field(default=None, alias="targetAmount")
    current_amount: Optional[StrictStr] = Field(default=None, alias="currentAmount")
    milestones: Optional[List[Milestone]] = None
    forecasts: Optional[Forecast] = None
    notes: Optional[List[SmartNote]] = None
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    __properties: ClassVar[List[str]] = ["id", "userId", "name", "description", "isCompleted", "goalType", "duration", "startDate", "endDate", "targetAmount", "currentAmount", "milestones", "forecasts", "notes", "createdAt", "deletedAt"]

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
        """Create an instance of SmartGoal from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in milestones (list)
        _items = []
        if self.milestones:
            for _item in self.milestones:
                if _item:
                    _items.append(_item.to_dict())
            _dict['milestones'] = _items
        # override the default output from pydantic by calling `to_dict()` of forecasts
        if self.forecasts:
            _dict['forecasts'] = self.forecasts.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in notes (list)
        _items = []
        if self.notes:
            for _item in self.notes:
                if _item:
                    _items.append(_item.to_dict())
            _dict['notes'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SmartGoal from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "userId": obj.get("userId"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "isCompleted": obj.get("isCompleted"),
            "goalType": obj.get("goalType") if obj.get("goalType") is not None else GoalType.UNSPECIFIED,
            "duration": obj.get("duration"),
            "startDate": obj.get("startDate"),
            "endDate": obj.get("endDate"),
            "targetAmount": obj.get("targetAmount"),
            "currentAmount": obj.get("currentAmount"),
            "milestones": [Milestone.from_dict(_item) for _item in obj["milestones"]] if obj.get("milestones") is not None else None,
            "forecasts": Forecast.from_dict(obj["forecasts"]) if obj.get("forecasts") is not None else None,
            "notes": [SmartNote.from_dict(_item) for _item in obj["notes"]] if obj.get("notes") is not None else None,
            "createdAt": obj.get("createdAt"),
            "deletedAt": obj.get("deletedAt")
        })
        return _obj


