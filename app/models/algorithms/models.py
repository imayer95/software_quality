"""
Model implementations for the stored algorithms.
"""

from app.models.algorithms.meta_model import Model, FieldNecessity, FieldType


class PythonSumModel(Model):
    """
    ORDER of field declaration is important
    """
    param1 = Model.Field('param1', FieldNecessity.REQUIRED, FieldType.INT)
    param2 = Model.Field('array', FieldNecessity.REQUIRED, FieldType.ARRAY)

    def __init__(self):
        pass

    def fields(self):
        return [self.__getattribute__(attr) for attr in dir(self)
                if not callable(getattr(self, attr))
                and not attr.startswith("__")]


class JavaSumModel(Model):
    """
    ORDER of field declaration is important
    """
    param1 = Model.Field('param1', FieldNecessity.REQUIRED, FieldType.INT)
    param2 = Model.Field('array', FieldNecessity.REQUIRED, FieldType.ARRAY)

    def __init__(self):
        pass

    def fields(self):
        return [self.__getattribute__(attr) for attr in dir(self)
                if not callable(getattr(self, attr))
                and not attr.startswith("__")]


class BFSModel(Model):
    """
    ORDER of field declaration is important
    """
    param1 = Model.Field('param1', FieldNecessity.REQUIRED, FieldType.INT)

    def __init__(self):
        pass

    def fields(self):
        return [self.__getattribute__(attr) for attr in dir(self)
                if not callable(getattr(self, attr))
                and not attr.startswith("__")]


class DFSModel(Model):
    """
    ORDER of field declaration is important
    """
    param1 = Model.Field('param1', FieldNecessity.REQUIRED, FieldType.INT)

    def __init__(self):
        pass

    def fields(self):
        return [self.__getattribute__(attr) for attr in dir(self)
                if not callable(getattr(self, attr))
                and not attr.startswith("__")]


class Mappings(object):
    """
    Mappings between the stored algorithm name (Case Sensitive, exact match) and the model.
    """
    PythonSum = PythonSumModel()
    JavaSum = JavaSumModel()
    BFS = BFSModel()
    DFS = DFSModel()
