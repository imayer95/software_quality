"""
Settings and configuration for the server.
"""
import os
import platform

APP_DIRECTORY = os.getcwd()+'/'
ALGORITHM_ROOT_DIRECTORY = APP_DIRECTORY + 'res/algorithms/'
JAVA_DIRECTORY = ALGORITHM_ROOT_DIRECTORY + 'java/'
PYTHON_DIRECTORY = ALGORITHM_ROOT_DIRECTORY + 'python/'
TEMP_COMPILATION_DIRECTORY = APP_DIRECTORY + 'temp/'

AFFORDABLE_INT_LIMIT = 1000000000
MULTIPLY_FACTOR = 10
RUN_TIME_LIMIT = 180


if 'win' in str(platform.system()).lower() and '/' in APP_DIRECTORY:
    APP_DIRECTORY = APP_DIRECTORY.replace('/', '\\')
    ALGORITHM_ROOT_DIRECTORY = ALGORITHM_ROOT_DIRECTORY.replace('/', '\\')
    JAVA_DIRECTORY = JAVA_DIRECTORY.replace('/', '\\')
    PYTHON_DIRECTORY = PYTHON_DIRECTORY.replace('/', '\\')
    TEMP_COMPILATION_DIRECTORY = TEMP_COMPILATION_DIRECTORY.replace('/', '\\')
