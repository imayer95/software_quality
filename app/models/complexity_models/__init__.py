
class Complexity(object):
    def __init__(self):
        pass

    def approximate(self, time_minus_1, last_time, multiplication_factor):
        pass

    def almost_equal(self, first, second):
        difference = second - first

        if abs(difference) <= 50:
            return True
        if not len(str(first)) == len(str(second)):
            return False
        else:
            difference = second - first
            if not difference < 7*10**(len(str(second))-1):
                return False
        return True
