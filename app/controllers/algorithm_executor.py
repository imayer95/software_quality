"""
Module that is responsible for executing stored algorithms.
"""

import subprocess

from app import settings
from app.models.algorithms.meta_model import Model
import app.models.algorithms.models as algorithm_models


class AlgorithmExecutor(object):
    """
    Class responsible for executing the given algorithm.
    """

    def __init__(self, algorithm_name: str):
        """
        Constructor.
        :param algorithm_name: the name of the stored algorithm.
        """
        self._algo = algorithm_name

    def execute(self, language: str, path: str, formatted_input: str):
        """
        Method that executes the provided algorithm.
        :param language: the language in which the algorithm is writen.
        :param path: the path to the source code of the algorithm.
        :param formatted_input: the input data for the algorithm.
        :return:
        """

        # If the language is python then simply run the script with process calls.
        if language == 'python':
            cmd = 'python' + ' ' + path + '.py ' + formatted_input
            print("CMD> ", cmd)

            child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output, error = child.communicate()
            return output, error

        # If the language is Java then first compile the program and then run the .class file
        elif language == 'java':

            cmd = 'javac' + ' ' + path + '.java '
            print("CMD> ", cmd)

            child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = child.communicate()[0]

            cmd = 'java -classpath ' + settings.JAVA_DIRECTORY + ' ' + self._algo + ' ' + formatted_input
            print("CMD> ", cmd)

            child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = child.communicate()
            return output, error


class Algorithm(object):
    """
    Model class for an algorithm.
    """

    def __init__(self, algo):
        """
        Constructor.
        :param algo: the name of the algorithm
        """
        self.algo = algo
        self.__model = self.__retrieve_model(self.algo)
        self._executor = AlgorithmExecutor(self.algo)

    def get_formatted_input(self, given_input: dict):
        """
        Method for transforming a dictionary into a format supported by script arguments.
        :param given_input: The dictionary with the input data
        :return: returns a string representation of the data that is accepted by the command line.
        """
        formatted_input = ''
        for field in self.__model.fields():
            if field.type() is list:
                for item in given_input[field.name()]:
                    formatted_input += str(item) + ' '
            else:
                formatted_input += str(given_input[field.name()]) + ' '
        return formatted_input

    def get_parameter_model(self):
        """
        Returns a list of the parameters related to the algorithm model.
        """

        fields = self.__model.fields()
        field_list = []
        for field in fields:
            field_list.append(field.dict_repr())
        return field_list

    def validate_input(self, given_input: dict) -> bool:
        """
        Validates that the given input matches the parameters model described.
        :param given_input: a set of input values for the algorithm.
        :return: return true if the input is valid, false otherwise.
        """

        for field in self.__model.fields():
            if field.is_required():
                if field.name() not in given_input:
                    return False
                else:
                    if not field.type() == type(given_input[field.name()]):
                        return False
        return True

    def execute(self, language: str, path: str, formatted_input: str):
        """
        Execute the given algorithm with the input data.
        :param language: The language of the algorithm
        :param path: The path to the source file of the algorithm
        :param formatted_input: the input for the algorithm.
        :return:
        """
        output, error = self._executor.execute(language, path, formatted_input)
        if error:
            return error.decode()
        else:
            return output.decode()

    @staticmethod
    def __retrieve_model(algo: str) -> Model:
        """
        Retrieves the model corresponding to the given algorithm name.
        :param algo: the name of the algorithm
        :return: returns the model of the given algorithm.
        """
        model = algorithm_models.Mappings.__dict__[algo]
        return model
