from app.models.algorithms.meta_model import Model, FieldNecessity, FieldType


class Test1Model(Model):
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


class Test2Model(Model):
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


class Mappings(object):
    test1 = Test1Model()
    test2 = Test2Model()
