"""
module that handles the subprocess calls of the system
"""
import os
import subprocess

from app import settings


class AlgorithmExecutor(object):
    """
    
    """

    def __init__(self, algorithm_name: str):
        self._algo = algorithm_name

    def execute(self, language: str, path: str, formatted_input: str):
        if language == 'python':
            cmd = 'python' + ' ' + path + '.py ' + formatted_input
            print("CMD> ", cmd)

            child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = child.communicate()[0]
            return output
        elif language == 'java':

            cmd = 'javac' + ' ' + path + '.java '
            print("CMD> ", cmd)

            child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = child.communicate()[0]

            cmd = 'java -classpath ' + settings.JAVA_DIRECTORY + ' ' + self._algo + ' ' + formatted_input
            print("CMD> ", cmd)

            child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = child.communicate()[0]
            return output
