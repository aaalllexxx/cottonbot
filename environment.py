from ast import literal_eval
from os import PathLike
from typing import Union

import dotenv
from enum import Enum


class DataTypes(Enum):
    int = 1
    float = 2
    str = 3
    auto = 4


class Environment:
    __convert_functions = {
        "int": int,
        "float": float,
        "str": str,
        "auto": literal_eval
    }

    def __init__(self, path: Union[str, PathLike]):
        items = dotenv.dotenv_values(path).items()
        for key, value in items:
            self.__dict__[key.lower()] = value

    def get_key(self, key, datatype: Union[str, DataTypes] = DataTypes.auto):
        try:
            return self.__convert_functions[(lambda x: x.name if isinstance(x, DataTypes) else x)(datatype)](
                self.__dict__[key.lower()])
        except SyntaxError:
            return self.__dict__[key.lower()]

    def __getattribute__(self, item):
        obj = super().__getattribute__(item)
        try:
            if not ("|:type=" in obj):
                return literal_eval(obj)
            else:
                args = obj.split("|:type=")
                if args[1] in list(self.__convert_functions):
                    return self.__convert_functions[args[1]](args[0])
                else:
                    return literal_eval(obj.split("|:type=")[0])

        except (ValueError, SyntaxError):
            return obj.split("|:type=")[0] if isinstance(obj, str) else obj

    def __getitem__(self, item):
        return self.__getattribute__(item)
