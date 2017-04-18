"""


"""
from typing import Iterable


class FieldNecessity(object):
    REQUIRED = 0
    OPTIONAL = 1


class FieldType(object):
    INT = int
    STRING = str
    ARRAY = list


class Model(object):
    """
    
    """

    class Field(object):
        """
        
        """

        def __init__(self, name:str, necessity: FieldNecessity, type: FieldType):
            self.__name = name
            self.__necessity = necessity
            self.__type = type

        def is_required(self):
            return True if self.__necessity == 0 else False

        def type(self):
            return self.__type

        def name(self):
            return self.__name

    def fields(self) -> Iterable[Field]:
        pass