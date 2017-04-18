"""
Settings and configuration for the server.
"""
import os
import platform


ALGORITHM_ROOT_DIRECTORY = os.getcwd()+'/'+'res/algorithms/'
JAVA_DIRECTORY = ALGORITHM_ROOT_DIRECTORY + 'java/'
PYTHON_DIRECTORY = ALGORITHM_ROOT_DIRECTORY + 'python/'


if 'win' in str(platform.system()).lower():
    ALGORITHM_ROOT_DIRECTORY = ALGORITHM_ROOT_DIRECTORY.replace('/', '\\')
    JAVA_DIRECTORY = JAVA_DIRECTORY.replace('/', '\\')
    PYTHON_DIRECTORY = PYTHON_DIRECTORY.replace('/', '\\')
