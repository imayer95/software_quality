"""
Module for getting the required algo file.
"""
import os
import platform
import sys
from typing import Iterable, Tuple

from app.models.Exceptions.exceptions import AlgorithmNotFound
from app.utils.platform_specific import format_path
from ..settings import *


class AlgorithmRepository(object):
    """
    
    """

    def __init__(self):
        pass

    @staticmethod
    def __list_dir(path: str) -> Iterable[str]:
        ls = os.listdir(path)
        try:
            ls.remove('__init__.py')
        except ValueError:
            pass
        return ls

    @staticmethod
    def get_algorithm_path(algorithm_name: str) -> Tuple[str, str]:
        for class_ in AlgorithmRepository.__list_dir(ALGORITHM_ROOT_DIRECTORY):
            for item in AlgorithmRepository.__list_dir(ALGORITHM_ROOT_DIRECTORY + class_):
                if item.split('.')[0].upper().strip() == algorithm_name.upper().strip():
                    algorithm_path = ALGORITHM_ROOT_DIRECTORY+class_+'/'+item.split('.')[0]
                    return algorithm_path, class_
        raise AlgorithmNotFound()
