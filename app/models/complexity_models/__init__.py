"""
Base complexity model.
"""


class Complexity(object):
    """
    Base complexity model class.
    """

    def approximate(self, time_minus_1, last_time, multiplication_factor):
        """
        Abstract method used to approximate the values to a specific complexity.
        :param time_minus_1: The before the last time value
        :param last_time: The last time value.
        :param multiplication_factor: The multiplication factor by which the input set increased.
        :return: returns true if the last two time values match the complexity rule, false otherwise.
        """
        pass

    def almost_equal(self, first, second):
        """
        Approximates if two numbers are almost equal
        For example 7890 and 7810 are almost equal.
        :param first: the first number.
        :param second: the second number.
        :return: returns true if the numbers are almost equal, false otherwise.
        """
        difference = second - first  # computes the difference between the two numbers.

        # if the difference is less then 50, returns true.
        if abs(difference) <= 50:
            return True

        # if the numbers have different number of digits, returns false.
        if not len(str(first)) == len(str(second)):
            return False

        # else if the difference multiplied is approximated to the second one, returns true.
        else:
            difference = second - first
            if not difference < 7 * 10 ** (len(str(second)) - 1):
                return False
        return True
