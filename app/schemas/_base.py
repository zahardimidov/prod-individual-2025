from collections import namedtuple
from enum import Enum
from typing import Any, ClassVar, Self, Type, get_type_hints

from pydantic import BaseModel, ConfigDict, GetCoreSchemaHandler
from pydantic import NonNegativeFloat as NNFloat
from pydantic import NonNegativeInt as NNInt
from pydantic_core import CoreSchema, core_schema


def get_cls_fields_type(cls: BaseModel):
    annotations = get_type_hints(cls)

    data = {k: v.annotation for k, v in cls.model_fields.items()}

    for k, v in annotations.items():
        if v.__dict__.get('_name') == 'Optional':
            class_ = v.__dict__.get('__args__', [str])[0]
        else:
            class_ = v
        data[k] = class_

    return namedtuple('fields', data.keys())(**data)



class RequestModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

    fields: ClassVar[Self]

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        _fields = get_cls_fields_type(cls)
        setattr(cls, "fields", _fields)


class IgnoreCaseEnum(str, Enum):
    @classmethod
    def _missing_(cls, value: str):
        normalized_value = value.lower()
        for member in cls:
            if str(member.value).lower() == normalized_value:
                return member


class CustomField:
    type: Type

    @classmethod
    def validation(cls, value):
        return value

    @classmethod
    def validate(cls, value, strict=True):
        if strict:
            return cls.validation(value)
        try:
            return cls.validation(value)
        except:
            ...

    def __new__(cls, value):
        return cls.validate(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(cls.type))


class NonEmptyStr(CustomField):
    type = str

    @classmethod
    def validation(cls, value):
        if len(value) == 0:
            raise ValueError('Передана пустая строка')
        return value


class NonNegativeInt(CustomField):
    type = NNInt

    @classmethod
    def validation(cls, value):
        if int(value) < 0:
            raise ValueError("Передано недопустимое значение")
        return int(value)


class NonNegativeFloat(CustomField):
    type = NNFloat

    @classmethod
    def validation(cls, value):
        if float(value) < 0:
            raise ValueError("Передано недопустимое значение")
        return float(value)
    


class Age(CustomField):
    type = NNInt

    @classmethod
    def validation(cls, value):
        if 0 <= int(value) <= 125:
            return int(value)
        raise ValueError('Передано недопустимое значение. Возраста должен пренадлежать промежутку от 0 до 125')