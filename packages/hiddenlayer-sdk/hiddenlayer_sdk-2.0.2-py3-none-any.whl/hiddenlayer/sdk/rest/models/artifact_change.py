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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from hiddenlayer.sdk.rest.models.artifact_location import ArtifactLocation
from hiddenlayer.sdk.rest.models.property_bag import PropertyBag
from hiddenlayer.sdk.rest.models.replacement import Replacement
from typing import Optional, Set
from typing_extensions import Self

class ArtifactChange(BaseModel):
    """
    A change to a single artifact.
    """ # noqa: E501
    artifact_location: ArtifactLocation = Field(alias="artifactLocation")
    replacements: Annotated[List[Replacement], Field(min_length=1)] = Field(description="An array of replacement objects, each of which represents the replacement of a single region in a single artifact specified by 'artifactLocation'.")
    properties: Optional[PropertyBag] = None
    __properties: ClassVar[List[str]] = ["artifactLocation", "replacements", "properties"]

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
        """Create an instance of ArtifactChange from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of artifact_location
        if self.artifact_location:
            _dict['artifactLocation'] = self.artifact_location.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in replacements (list)
        _items = []
        if self.replacements:
            for _item in self.replacements:
                if _item:
                    _items.append(_item.to_dict())
            _dict['replacements'] = _items
        # override the default output from pydantic by calling `to_dict()` of properties
        if self.properties:
            _dict['properties'] = self.properties.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ArtifactChange from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "artifactLocation": ArtifactLocation.from_dict(obj["artifactLocation"]) if obj.get("artifactLocation") is not None else None,
            "replacements": [Replacement.from_dict(_item) for _item in obj["replacements"]] if obj.get("replacements") is not None else None,
            "properties": PropertyBag.from_dict(obj["properties"]) if obj.get("properties") is not None else None
        })
        return _obj


