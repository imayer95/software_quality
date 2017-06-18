from math import log10

from app.models.complexity_models import Complexity


class OOfLogN(Complexity):
    def approximate(self, time_minus_1, last_time, multiplication_factor):
        time_minus_1 = time_minus_1 * log10(multiplication_factor+18)

        return self.almost_equal(time_minus_1, last_time)

    def __str__(self):
        return 'O(log n)'
