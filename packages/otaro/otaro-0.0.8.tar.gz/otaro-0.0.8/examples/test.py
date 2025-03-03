from enum import Enum
from typing import Literal, Type, get_args, get_origin

from pydantic import BaseModel


class Status(Enum):
    todo = "todo"
    complete = "complete"


class Animal(BaseModel):
    name: str
    num_legs: int


class Step(BaseModel):
    number: int
    desc: str
    status: Status
    people: Literal["adam", "beth"]
    animal: Animal


brands = Literal["apple", "microsoft"]


def field_type_to_dict(field_type: Type):
    if field_type in [str, int, float, bool]:
        return field_type.__name__
    elif get_origin(field_type) == Literal:
        args = get_args(field_type)
        return list(args)
    elif issubclass(field_type, Enum):
        return list(map(lambda c: c.name, field_type))
    elif field_type == list:
        return "list"
    elif get_origin(field_type) == list:
        child_type = get_args(field_type)[0]
        return f"list[{field_type_to_dict(child_type)}]"
    elif issubclass(field_type, BaseModel):
        attrs = {}
        for field_name, field_info in field_type.model_fields.items():
            attrs[field_name] = field_type_to_dict(field_info.annotation)
        return attrs


print(field_type_to_dict(Step))
print(Step.model_json_schema())
print(brands("apple"))
print(brands("apples"))
