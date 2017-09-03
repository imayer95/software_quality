"""
Module responsible for generating various different random data.
"""

import random


class IntGenerator(object):
    """
    A class that generates random integer values.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.last_generated_value = -1
        self._multiplication_factor = 1

    def random(self, min_=0, max_=100):
        """
        Returns a random number between min and max.
        :param min_: The lowest possible value of the random integer.
        :param max_: The highest possible value of the random integer.
        :return: Returns a random number between min and max.
        """
        return random.randint(min_, max_)

    def random_multiplier(self, min_=0, max_=100):
        """
        Generates a number between min and max and then multiplies it with the multiplication factor
        :param min_: The lowest possible value of the random integer.
        :param max_: The highest possible value of the random integer.
        :return: Returns a random number between min and max multiplied with the multiplication factor.
        """
        self.last_generated_value = random.randint(min_, max_) * self._multiplication_factor
        return self.last_generated_value

    def increase_multiplication_factor(self, multiplication_factor):
        """
        Increase the multiplication factor.
        :param multiplication_factor: the value by which to increase.
        """
        self._multiplication_factor = self._multiplication_factor * multiplication_factor

    def next_multiplied_value(self):
        """
        Uses the last random generated value and multiplies it with the multiplication factor.
        :return: returns the new multiplied random value.
        """
        self.last_generated_value = self.last_generated_value * self._multiplication_factor
        return self.last_generated_value


class RandomDataGenerator(object):
    """
    Random data generator for algorithm parameters.
    """

    def __init__(self, pattern, value_limit, multiply_factor):
        """
        Constructor.
        :param pattern: The pattern for the parameters. (meta-model for the parameters).
        :param value_limit: The upper limit for int values.
        :param multiply_factor: the multiplication factor by which to increase the random values.
        """
        self._multiply_factor = multiply_factor
        self._pattern = pattern
        self._value_limit = value_limit
        self._initial_multiplier = 1
        self.__array_range = 50
        self._int_generator = IntGenerator()

    def next(self):
        """
        Validator. Checks if a new multiplied random number can be generated.
        :return: returns true if a new multiplied random number can be generated, otherwise false.
        """
        return self._int_generator.last_generated_value < self._value_limit

    def __enlarge(self, number, multiplier, pattern=None):
        """
        Based on the description of the current parameter, it doubles the values of the number or it multiplies it.
        :param number: The number to be increased.
        :param multiplier: the multiplier
        :param pattern: the type of enlargement (linear OR exponential).
        :return: returns the modified number.
        """
        if pattern == 'linear':
            return number * 2
        else:
            return number * multiplier

    def get_random_data(self):
        """
        Generates a set of random data for the given pattern (the list of parameters with their customizations).
        :return: return a dictionary with the  generated values for each parameter based on the specification in the pattern.
        """
        input_data = dict()
        for index in range(0, len(self._pattern)):
            param = self._pattern[index]  # get the current parameter.

            # If the parameter represents an integer:
            if param['type'] == 'int':
                if 'static_value' in param:
                    input_data['param' + str(index + 1)] = param['static_value']
                else:
                    input_data['param' + str(index + 1)] = self.__enlarge(10, self._initial_multiplier, param['growth'])
                    self._int_generator.last_generated_value = self.__enlarge(150, self._initial_multiplier,
                                                                              param['growth'])

            # If the parameter represents an array, create a list of random integers.
            elif param['type'] == 'array':
                array_list = list()

                for i in range(0, self.__array_range):
                    array_list.append(self._int_generator.random(0, 1000))
                input_data['param' + str(index + 1)] = array_list
                self.__array_range = self.__array_range * 2

        self._initial_multiplier = self._initial_multiplier * self._multiply_factor
        self._int_generator.increase_multiplication_factor(self._multiply_factor)
        return input_data
