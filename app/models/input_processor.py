"""

"""


class InputFormatter(object):
    def __init__(self):
        pass

    def format_from_dict(self, input_data):
        formatted_input = ''
        for key in input_data:
            if isinstance(input_data[key], list):

                for item in input_data[key]:
                    formatted_input += str(item) + ' '
            else:
                formatted_input += str(input_data[key]) + ' '
        print('WWWWWWWWWWWWWWWWWWWWWWWWWW ', formatted_input)
        return formatted_input
