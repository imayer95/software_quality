"""
Module for formatting different kinds of data.
"""


class InputFormatter(object):
    """
    Class for transforming data structures into a format supported by script arguments.
    """

    def format_from_dict(self, input_data):
        """
        Method for transforming a dictionary into a format supported by script arguments.
        :param input_data: The dictionary with the input data
        :return: returns a string representation of the data that is accepted by the command line.
        """
        formatted_input = ''
        for key in input_data:

            # If the value for the current key is a list, concat the elements from the list into a string.
            if isinstance(input_data[key], list):

                for item in input_data[key]:
                    formatted_input += str(item) + ' '

            # Add the current value to the string.
            else:
                formatted_input += str(input_data[key]) + ' '

        return formatted_input
