from enum import Enum
from typing import Any, List

import jsonref
from pydantic import BaseModel, create_model

Types = {"integer": int, "string": str, "boolean": bool}


def parse(obj: dict[str, Any]) -> type[BaseModel]:
    """Convert JSON Schema to Pydantic model

    Args:
        obj (dict[str, Any]): Model JSON Schema

    Returns:
        type[BaseModel]: Resulting Pydantic model
    """

    def _parse_list(title: str, obj: dict[str, dict[str, dict]]) -> type[BaseModel]:
        match obj.get("type", "enum"):
            case "object":
                return _parse_object(obj["title"], obj["properties"])
            case "array":
                return List[_parse_list(title, obj["items"])]
            case _:
                if obj.get("enum"):
                    return Enum(
                        obj["title"], {item.upper(): item for item in obj["enum"]}
                    )
                else:
                    return Types[obj["type"]]

    def _parse_object(
        title: str, obj: dict[str, dict[str, dict]], res={}
    ) -> type[BaseModel]:
        """Convert JSON Schema to Pydantic model

        Args:
            title (str): Pydantic class name
            obj (dict[str, dict[str, dict]]): Properties JSON Schema
            res (dict, optional): _description_. Defaults to {}.

        Returns:
            type[BaseModel]: _description_
        """
        for k, v in obj.items():
            match v.get("type", "enum"):
                case "object":
                    res = res | {k: (_parse_object(v["title"], v["properties"]), None)}
                case "array":
                    res = res | {k: (List[_parse_list(v["title"], v["items"])], None)}
                case _:
                    if v.get("enum"):
                        res = res | {
                            k: (
                                Enum(
                                    v["title"],
                                    {item.upper(): item for item in v.get("enum")},
                                ),
                                None,
                            )
                        }
                    else:
                        res = res | {k: (Types[v["type"]], None)}

        return create_model(title, **res)

    obj = jsonref.replace_refs(obj)
    return _parse_object(obj["title"], obj["properties"])
