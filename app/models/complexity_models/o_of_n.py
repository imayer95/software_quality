from app.models.complexity_models import Complexity


class OOfN(Complexity):
    def approximate(self, time_minus_1, last_time, multiplication_factor):
        time_minus_1 = time_minus_1 * multiplication_factor
        return self.almost_equal(time_minus_1, last_time)

    def __str__(self):
        return 'O(n)'
