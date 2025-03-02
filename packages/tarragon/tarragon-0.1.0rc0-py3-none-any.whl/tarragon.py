import json
from typing import Any


class DictRepresentor:
    @classmethod
    def __get_collection_representation(cls, collection: list | tuple | set) -> list:
        result = []
        for item in collection:
            result.append(cls.get_representation(item))
        return result

    @classmethod
    def get_representation(cls, obj: Any) -> int | float | bool | str | list | dict:
        obj_type = type(obj)
        if obj_type in [int, float, bool, str]:
            return obj
        elif obj_type is list:
            return cls.__get_collection_representation(obj)
        elif obj_type in [tuple, set]:
            array = cls.__get_collection_representation(obj)
            return {
                "type": obj_type.__name__,
                "array": array
            }
        elif obj_type is dict:
            items = []
            for key, value in obj.items():
                items.append({
                    "key": cls.get_representation(key),
                    "value": cls.get_representation(value)
                })
            return {
                "type": obj_type.__name__,
                "items": items
            }
        else:
            # If custom class
            fields = {}
            for key, value in vars(obj).items():
                fields[key] = cls.get_representation(value)
            return {
                "type": obj_type.__module__ + "." + obj_type.__name__,
                "object": fields
            }


def to_json(obj: Any) -> str:
    return json.dumps(DictRepresentor.get_representation(obj))


def from_json(json: str) -> Any:
    raise NotImplementedError()


def to_yaml(obj: Any) -> str:
    raise NotImplementedError()


def from_yaml(yaml: str) -> Any:
    raise NotImplementedError()


def to_xml(obj: Any) -> str:
    raise NotImplementedError()


def from_xml(xml: str) -> Any:
    raise NotImplementedError()
