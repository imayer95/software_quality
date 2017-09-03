"""
Module for getting the required algo file.
"""

from typing import Iterable, Tuple

from app.models.Exceptions.exceptions import AlgorithmNotFound
from ..settings import *


class AlgorithmRepository(object):
    """
    Algorithm repository class.
    """

    @staticmethod
    def __list_dir(path: str) -> Iterable[str]:
        """
        Lists the content of a given path without the __init__.py file.
        :param path:
        :return:
        """
        ls = os.listdir(path)
        try:
            ls.remove('__init__.py')
        except ValueError:
            pass
        return ls

    @staticmethod
    def get_algorithm_path(algorithm_name: str) -> Tuple[str, str]:
        """
        Returns the path to the source file of the algorithm by name.
        :param algorithm_name: the name of the algorithm.
        :return: return the path to the source file of the algorithm.
        """
        for class_ in AlgorithmRepository.__list_dir(ALGORITHM_ROOT_DIRECTORY):
            for item in AlgorithmRepository.__list_dir(ALGORITHM_ROOT_DIRECTORY + class_):
                if item.split('.')[0].upper().strip() == algorithm_name.upper().strip():
                    algorithm_path = ALGORITHM_ROOT_DIRECTORY + class_ + '/' + item.split('.')[0]
                    return algorithm_path, class_
        raise AlgorithmNotFound()
