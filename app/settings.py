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
RUN_TIME_LIMIT = 120
