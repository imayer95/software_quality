"""
Model for the O(n) complexity
"""

from app.models.complexity_models import Complexity


class OOfN(Complexity):
    """
    Class modeling the O(n) complexity.
    RULE for O(n):
    * last_time = previous_time * multiplication_factor.
    """

    def approximate(self, time_minus_1, last_time, multiplication_factor):
        """
        Method that tries to match the given times to the O(n) rule.
        :param time_minus_1: The before the last time value
        :param last_time: The last time value.
        :param multiplication_factor: The multiplication factor by which the input set increased.
        :return: returns true if the last two time values match the complexity rule, false otherwise.
        """
        time_minus_1 = time_minus_1 * multiplication_factor
        return self.almost_equal(time_minus_1, last_time)

    def __str__(self):
        return 'O(n)'
