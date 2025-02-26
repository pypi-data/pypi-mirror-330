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
from hiddenlayer.sdk.rest.models.edge_traversal import EdgeTraversal
from hiddenlayer.sdk.rest.models.message import Message
from hiddenlayer.sdk.rest.models.multiformat_message_string import MultiformatMessageString
from hiddenlayer.sdk.rest.models.property_bag import PropertyBag
from typing import Optional, Set
from typing_extensions import Self

class GraphTraversal(BaseModel):
    """
    Represents a path through a graph.
    """ # noqa: E501
    run_graph_index: Optional[Annotated[int, Field(strict=True, ge=-1)]] = Field(default=-1, description="The index within the run.graphs to be associated with the result.", alias="runGraphIndex")
    result_graph_index: Optional[Annotated[int, Field(strict=True, ge=-1)]] = Field(default=-1, description="The index within the result.graphs to be associated with the result.", alias="resultGraphIndex")
    description: Optional[Message] = None
    initial_state: Optional[Dict[str, MultiformatMessageString]] = Field(default=None, description="Values of relevant expressions at the start of the graph traversal that may change during graph traversal.", alias="initialState")
    immutable_state: Optional[Dict[str, MultiformatMessageString]] = Field(default=None, description="Values of relevant expressions at the start of the graph traversal that remain constant for the graph traversal.", alias="immutableState")
    edge_traversals: Optional[Annotated[List[EdgeTraversal], Field(min_length=0)]] = Field(default=None, description="The sequences of edges traversed by this graph traversal.", alias="edgeTraversals")
    properties: Optional[PropertyBag] = None
    __properties: ClassVar[List[str]] = []

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
        """Create an instance of GraphTraversal from a JSON string"""
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
        """Create an instance of GraphTraversal from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
        })
        return _obj


