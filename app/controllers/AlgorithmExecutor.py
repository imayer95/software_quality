import subprocess

from app import settings
from app.models.algorithms.meta_model import Model
import app.models.algorithms.models as algorithm_models


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
            output, error = child.communicate()
            return output, error
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

    """

    def __init__(self, algo):
        self.algo = algo
        self.__model = self.__retrieve_model(self.algo)
        self._executor = AlgorithmExecutor(self.algo)

    def get_formatted_input(self, given_input: dict):
        formatted_input = ''
        for field in self.__model.fields():
            if field.type() is list:
                for item in given_input[field.name()]:
                    formatted_input += str(item) + ' '
            else:
                formatted_input += str(given_input[field.name()]) + ' '
        return formatted_input

    def get_parameter_model(self):
        fields = self.__model.fields()
        field_list = []
        for field in fields:
            field_list.append(field.dict_repr())
        return field_list

    def validate_input(self, given_input: dict) -> bool:

        for field in self.__model.fields():
            if field.is_required():
                if field.name() not in given_input:
                    return False
                else:
                    if not field.type() == type(given_input[field.name()]):
                        return False
        return True

    def execute(self, language: str, path: str, formatted_input: str):
        output, error = self._executor.execute(language, path, formatted_input)
        if error:
            return error.decode()
        else:
            return output.decode()

    @staticmethod
    def __retrieve_model(algo: str) -> Model:
        model = algorithm_models.Mappings.__dict__[algo]
        return model
