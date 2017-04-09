"""
Settings and configuration for the server.
"""
import platform


ALGORITHM_ROOT_DIRECTORY = 'res/algorithms/'


if 'win' in str(platform.system()).lower():
    ALGORITHM_ROOT_DIRECTORY = ALGORITHM_ROOT_DIRECTORY.replace('/', '\\')
