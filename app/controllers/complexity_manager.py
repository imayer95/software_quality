from app.models.complexity_models.o_of_n import OOfN
from app.models.complexity_models.o_of_n_square import OOfNSquare


class ComplexityManager(object):
    def __init__(self, multiplication_factor):
        self._multiplication_factor = multiplication_factor
        self._complexities = list()
        self._complexities.append(OOfN())
        self._complexities.append(OOfNSquare())

    def get_complexity(self, time1, time2):
        for complexity in self._complexities:
            if complexity.approximate(time1, time2, self._multiplication_factor):
                return str(complexity)
