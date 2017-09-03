"""
Controller for managing the complexity computation.
"""

from app.models.complexity_models.o_of_log_n import OOfLogN
from app.models.complexity_models.o_of_n import OOfN
from app.models.complexity_models.o_of_n_square import OOfNSquare


class ComplexityManager(object):
    """
    Controller class for computing the complexity.
    """

    def __init__(self, multiplication_factor):
        """
        Constructor.
        :param multiplication_factor: The multiplication factor used in generating random values.
        """
        self._multiplication_factor = multiplication_factor
        self._complexities = list()
        self._complexities.append(OOfN())
        self._complexities.append(OOfNSquare())
        self._complexities.append(OOfLogN())

    def get_complexity(self, time1, time2):
        """
        Method that attempts to match the two times to a complexity.
        :param time1: The first time
        :param time2: The second time.
        :return: returns the name of the complexity.
        """
        for complexity in self._complexities:
            if complexity.approximate(time1, time2, self._multiplication_factor):
                return str(complexity)
