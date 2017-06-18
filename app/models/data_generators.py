"""

"""

import random


class IntGenerator(object):
    def __init__(self):
        self.last_generated_value = -1
        self._multiplication_factor = 1

    def random(self, min_=0, max_=100):
        return random.randint(min_, max_)

    def random_multiplier(self, min_=0, max_=100):
        self.last_generated_value = random.randint(min_, max_)*self._multiplication_factor
        return self.last_generated_value

    def increase_multiplication_factor(self, multiplication_factor):
        self._multiplication_factor = self._multiplication_factor * multiplication_factor

    def next_multiplied_value(self):
        self.last_generated_value = self.last_generated_value*self._multiplication_factor
        return self.last_generated_value


class RandomDataGenerator(object):
    def __init__(self, pattern, value_limit, multiply_factor):
        self._multiply_factor = multiply_factor
        self._pattern = pattern
        self._value_limit = value_limit
        self._initial_multiplier = 1
        self.__array_range = 50
        self._int_generator = IntGenerator()

    def next(self):
        return self._int_generator.last_generated_value < self._value_limit

    def __enlarge(self, number, multiplier, pattern=None):
        if pattern == 'linear':
            return number * 2
        else:
            return number * multiplier

    def get_random_data(self):
        input_data = dict()
        for index in range(0, len(self._pattern)):
            param = self._pattern[index]
            if param['type'] == 'int':
                if 'static_value' in param:
                    input_data['param' + str(index + 1)] = param['static_value']
                else:
                    input_data['param'+str(index+1)] = self.__enlarge(10, self._initial_multiplier, param['growth'])
                    self._int_generator.last_generated_value = self.__enlarge(150, self._initial_multiplier, param['growth'])

            elif param['type'] == 'array':
                array_list = list()

                for i in range(0, self.__array_range):
                    array_list.append(self._int_generator.random(0, 1000))
                input_data['param'+str(index+1)] = array_list
                self.__array_range = self.__array_range * 2

        self._initial_multiplier = self._initial_multiplier * self._multiply_factor
        self._int_generator.increase_multiplication_factor(self._multiply_factor)
        return input_data
