# coding: utf-8

"""
    HiddenLayer ModelScan V2

    HiddenLayer ModelScan API for scanning of models

    The version of the OpenAPI document: 1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from hiddenlayer.sdk.rest.models.message import Message
from hiddenlayer.sdk.rest.models.multiformat_message_string import MultiformatMessageString
from hiddenlayer.sdk.rest.models.property_bag import PropertyBag
from hiddenlayer.sdk.rest.models.thread_flow_location import ThreadFlowLocation
from typing import Optional, Set
from typing_extensions import Self

class ThreadFlow(BaseModel):
    """
    Describes a sequence of code locations that specify a path through a single thread of execution such as an operating system or fiber.
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="An string that uniquely identifies the threadFlow within the codeFlow in which it occurs.")
    message: Optional[Message] = None
    initial_state: Optional[Dict[str, MultiformatMessageString]] = Field(default=None, description="Values of relevant expressions at the start of the thread flow that may change during thread flow execution.", alias="initialState")
    immutable_state: Optional[Dict[str, MultiformatMessageString]] = Field(default=None, description="Values of relevant expressions at the start of the thread flow that remain constant.", alias="immutableState")
    locations: Annotated[List[ThreadFlowLocation], Field(min_length=1)] = Field(description="A temporally ordered array of 'threadFlowLocation' objects, each of which describes a location visited by the tool while producing the result.")
    properties: Optional[PropertyBag] = None
    __properties: ClassVar[List[str]] = ["id", "message", "initialState", "immutableState", "locations", "properties"]

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
        """Create an instance of ThreadFlow from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of message
        if self.message:
            _dict['message'] = self.message.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in initial_state (dict)
        _field_dict = {}
        if self.initial_state:
            for _key in self.initial_state:
                if self.initial_state[_key]:
                    _field_dict[_key] = self.initial_state[_key].to_dict()
            _dict['initialState'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in immutable_state (dict)
        _field_dict = {}
        if self.immutable_state:
            for _key in self.immutable_state:
                if self.immutable_state[_key]:
                    _field_dict[_key] = self.immutable_state[_key].to_dict()
            _dict['immutableState'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each item in locations (list)
        _items = []
        if self.locations:
            for _item in self.locations:
                if _item:
                    _items.append(_item.to_dict())
            _dict['locations'] = _items
        # override the default output from pydantic by calling `to_dict()` of properties
        if self.properties:
            _dict['properties'] = self.properties.to_dict()
        # set to None if message (nullable) is None
        # and model_fields_set contains the field
        if self.message is None and "message" in self.model_fields_set:
            _dict['message'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ThreadFlow from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "message": Message.from_dict(obj["message"]) if obj.get("message") is not None else None,
            "initialState": dict(
                (_k, MultiformatMessageString.from_dict(_v))
                for _k, _v in obj["initialState"].items()
            )
            if obj.get("initialState") is not None
            else None,
            "immutableState": dict(
                (_k, MultiformatMessageString.from_dict(_v))
                for _k, _v in obj["immutableState"].items()
            )
            if obj.get("immutableState") is not None
            else None,
            "locations": [ThreadFlowLocation.from_dict(_item) for _item in obj["locations"]] if obj.get("locations") is not None else None,
            "properties": PropertyBag.from_dict(obj["properties"]) if obj.get("properties") is not None else None
        })
        return _obj


