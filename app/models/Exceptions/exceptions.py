"""
Module containing implementations for custom exceptions.
"""


class AlgorithmNotFound(Exception):
    """
    Exception representing the case when a stored algorithm was not found.
    """

    def __init__(self):
        super(AlgorithmNotFound, self).__init__("Requested algorithm not found on server.")
