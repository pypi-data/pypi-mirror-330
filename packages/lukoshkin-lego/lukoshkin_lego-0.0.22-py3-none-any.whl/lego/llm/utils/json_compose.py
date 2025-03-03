"""
An example of how tool calling can be used with a router:

```python
    router(
        prompt,  # type: list[dict[str, str]]
        tools=[model_to_tool(SomePydanticModel)],
        tool_choice=[convert_to_tool_choice(SomePydanticModel)],
    )
```
"""

import copy
from typing import Type, TypedDict

from pydantic import BaseModel

from lego.lego_types import JSONDict
from lego.llm.utils.parse import parse_json


class ResponseFormat(TypedDict):
    """Response format parameter for structured output OpenAI API calls."""

    type: str
    json_schema: JSONDict


def additional_properties_false(schema: JSONDict) -> JSONDict:
    """Recursively add to the schema 'additionalProperties': False."""
    schema = copy.deepcopy(schema)
    if schema.get("type") == "object":
        schema["additionalProperties"] = False

    if "properties" in schema:
        for _, prop_schema in schema["properties"].items():
            additional_properties_false(prop_schema)

    if schema.get("type") == "array" and "items" in schema:
        additional_properties_false(schema["items"])

    return schema


def response_format(pymodel: BaseModel, strict: bool = True) -> ResponseFormat:
    json_schema = pymodel.model_json_schema()
    return {
        "type": "json_schema",
        "json_schema": {
            "name": pymodel.__name__,
            "strict": strict,
            "schema": (
                additional_properties_false(json_schema)
                if strict
                else json_schema
            ),
        },
    }


def read_model(model: Type[BaseModel], model_json: str) -> BaseModel:
    """Create a pydantic model from a JSON string."""
    return model.model_validate(parse_json(model_json))


def model_to_tool(model: BaseModel) -> JSONDict:
    """Convert a Pydantic model to a tool."""
    json_schema = model.model_json_schema()
    desc = json_schema.pop("description", None)
    if desc is None:
        raise ValueError("Please add a docstring for the provided model.")

    return {
        "type": "function",
        "function": {
            "name": model.__class__.__name__,
            "description": desc,
            "parameters": json_schema,
        },
    }


def convert_to_tool_choice(tool: JSONDict | BaseModel) -> JSONDict:
    """Convert a tool or Pydantic model to a tool choice."""
    if isinstance(tool, BaseModel):
        return {
            "type": "function",
            "function": {"name": tool.__class__.__name__},
        }
    return {
        "type": "function",
        "function": {"name": tool["function"]["name"]},
    }
