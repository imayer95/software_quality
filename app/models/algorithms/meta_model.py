"""
Base class Model for all the Algorithm model classes.
"""
from typing import Iterable


class FieldNecessity(object):
    """
    Represents the necessity of the parameters.
    """
    REQUIRED = 0
    OPTIONAL = 1


class FieldType(object):
    """
    Represents the type of the parameter.
    """
    INT = int
    STRING = str
    ARRAY = list


class Model(object):
    """
    Base model class for algorithms.
    """

    class Field(object):
        """
        A model class for a field type.
        """

        def __init__(self, name: str, necessity: FieldNecessity, type: FieldType):
            """
            Constructor.
            :param name: The name of the field (parameter).
            :param necessity: the necessity of the parameter (is required OR optional).
            :param type: The type of the parameter (Int, Array... ).
            """
            self.__name = name
            self.__necessity = necessity
            self.__type = type

        def is_required(self):
            """
            Method that tells if the field is required or not.
            """
            return True if self.__necessity == 0 else False

        def type(self):
            """
            Method (Getter) that tells the type of the field.
            """
            return self.__type

        def name(self):
            """
            Method (Getter) that tells the name of the field.
            :return:
            """
            return self.__name

        def dict_repr(self):
            """
            Format the class values into a dictionary structure.
            """
            type_ = "int"
            if isinstance(self.__type, str):
                type_ = "str"
            if isinstance(self.__type, list):
                type_ = "array"
            dr = {"type": type_}
            return dr

        def __str__(self):
            type_ = "int"
            if isinstance(self.__type, str):
                type_ = "str"
            if isinstance(self.__type, list):
                type_ = "array"
            dr = {"type": type_}
            return str(dr)

        def __repr__(self):
            type_ = "int"
            if isinstance(self.__type, str):
                type_ = "str"
            if isinstance(self.__type, list):
                type_ = "array"
            dr = {"type": type_}
            return str(dr)

    def fields(self) -> Iterable[Field]:
        """
        Abstract method that returns a list of all the fields declared for the model.
        """
        pass
