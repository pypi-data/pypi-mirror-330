import pytest
from enum import Enum

from src.parsdantic.parser import parse


@pytest.mark.parametrize(
    "data, json_schema, expected",
    [
        (
            {"color": "RED"},
            {
                "type": "object",
                "title": "ColorModel",
                "properties": {
                    "color": {
                        "title": "Color",
                        "enum": ["RED", "GREEN", "BLUE"]
                    }
                }
            },
            True
        ),
        (
            {"color": "YELLOW"},  # Value not in enum
            {
                "type": "object",
                "title": "ColorModel",
                "properties": {
                    "color": {
                        "title": "Color",
                        "enum": ["RED", "GREEN", "BLUE"]
                    }
                }
            },
            False
        ),
        (
            {"status": "ACTIVE", "user_type": "ADMIN"},
            {
                "type": "object",
                "title": "UserModel",
                "properties": {
                    "status": {
                        "title": "Status",
                        "enum": ["ACTIVE", "INACTIVE", "PENDING"]
                    },
                    "user_type": {
                        "title": "UserType",
                        "enum": ["ADMIN", "USER", "GUEST"]
                    }
                }
            },
            True
        ),
        (
            {"person": {"role": "MANAGER"}},
            {
                "type": "object",
                "title": "EmployeeModel",
                "properties": {
                    "person": {
                        "title": "Person",
                        "type": "object",
                        "properties": {
                            "role": {
                                "title": "Role",
                                "enum": ["MANAGER", "DEVELOPER", "TESTER"]
                            }
                        }
                    }
                }
            },
            True
        ),
        (
            {"items": [{"category": "ELECTRONICS"}, {"category": "BOOKS"}]},
            {
                "type": "object",
                "title": "InventoryModel",
                "properties": {
                    "items": {
                        "title": "Items",
                        "type": "array",
                        "items": {
                            "title": "Item",
                            "type": "object",
                            "properties": {
                                "category": {
                                    "title": "Category",
                                    "enum": ["ELECTRONICS", "BOOKS", "CLOTHING"]
                                }
                            }
                        }
                    }
                }
            },
            True
        ),
        (
            {"items": [{"category": "ELECTRONICS"}, {"category": "FOOD"}]},  # FOOD not in enum
            {
                "type": "object",
                "title": "InventoryModel",
                "properties": {
                    "items": {
                        "title": "Items",
                        "type": "array",
                        "items": {
                            "title": "Item",
                            "type": "object",
                            "properties": {
                                "category": {
                                    "title": "Category",
                                    "enum": ["ELECTRONICS", "BOOKS", "CLOTHING"]
                                }
                            }
                        }
                    }
                }
            },
            False
        ),
    ]
)
def test_enum(data, json_schema, expected):
    try:
        pydantic_model = parse(json_schema)
        instance = pydantic_model(**data)
        pydantic_model.model_validate(instance)
        assert expected
    except Exception as e:
        assert not expected