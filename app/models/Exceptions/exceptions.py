"""

"""


class AlgorithmNotFound(Exception):
    """
    
    """

    def __init__(self):
        super(AlgorithmNotFound, self).__init__("Requested algorithm not found on server.")
