"""
Model for the O(log n) complexity
"""

from math import log10
from app.models.complexity_models import Complexity


class OOfLogN(Complexity):
    """
    Class modeling the O(log n) complexity.
    RULE for O(log n):
    * last_time = previous_time * log10(multiplication_factor).
    """

    def approximate(self, time_minus_1, last_time, multiplication_factor):
        """
        Method that tries to match the given times to the O(log n) rule.
        :param time_minus_1: The before the last time value.
        :param last_time: The last time value.
        :param multiplication_factor: The multiplication factor by which the input set increased.
        :return: returns true if the last two time values match the complexity rule, false otherwise.
        """

        time_minus_1 = time_minus_1 * log10(multiplication_factor + 18)
        return self.almost_equal(time_minus_1, last_time)

    def __str__(self):
        return 'O(log n)'
