"""
module that handles the subprocess calls of the system
"""
import os
import subprocess
import time

from app import settings
from app.models.input_processor import InputFormatter


class CompileStatus(dict):
    """
    A class that represents the status of a compilation process
    """

    def __init__(self, status, message, **kwargs):
        """
        Constructor.
        :param status: The status of the compilation
        :param message: The message of the compilation
        """
        super().__init__(**kwargs)
        self.status = status
        self.message = message
        self['status'] = status
        self['message'] = message

    def __str__(self):
        formal_data = dict(status=self.status,
                           message=self.message)
        return str(formal_data)


class ExecutionStatus(CompileStatus):
    """
    A class that represents the status of a execution process
    """

    def __init__(self, status, message, result, run_time):
        """
        Constructor.
        :param status: The status of the execution process
        :param message: The message of the execution process
        :param result: The result of the execution process
        :param run_time: The time it took to execute.
        """
        super().__init__(status, message)
        self.result = result
        self.run_time = run_time
        self['result'] = result
        self['run_time'] = run_time

    def __str__(self):
        formal_data = dict(status=self.status,
                           message=self.message,
                           result=self.result)
        return str(formal_data)


class Executor(object):
    """
    Base class for an executor.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._formatter = InputFormatter()

    def compile(self, source_code) -> CompileStatus:
        """
        Abstract method for compiling a program.
        :param source_code: the source code of the program.
s        """
        pass

    def execute(self, input_data) -> ExecutionStatus:
        """
        Abstract class for executing a program.
        :param input_data: Input data for the execution process.
        """
        pass

    def set_unique_id(self, id_):
        """
        Abstract method for generating an unique ID for the current task
        :param id_:
        :return:
        """
        pass

    def _run_process(self, cmd):
        """
        Execute a subprocess system call.
        :param cmd: The command to be executed by the child process.
        :return: returns an execution status object.
        """
        start = int(round(time.time() * 1000))
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output, error = child.communicate(timeout=300)
        except subprocess.TimeoutExpired:
            return None
        end = int(round(time.time() * 1000))
        output = output.decode()
        error = error.decode()
        if not error == '':
            return ExecutionStatus(False, 'Error execution program',
                                   error.replace('\r', '').replace('\n', '').replace('\t', ''), int(end - start))
        else:
            return ExecutionStatus(True, 'Execution done',
                                   output.replace('\r', '').replace('\n', '').replace('\t', ''), int(end - start))


class JavaExecution(Executor):
    """
    Specific executor for Java programs.
    """

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self.__unique_id = "-1"

    def set_unique_id(self, id_):
        """
        Set the unique ID for the task.
        :param id_: The ID to be set.
        """
        self.__unique_id = id_

    def compile(self, source_code) -> CompileStatus:
        """
        Method used to compile the given program.
        :param source_code: The source code for the program.
        :return: returns a compile status object
        """
        if not os.path.exists(settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id):
            os.mkdir(settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id)
        with open(settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id + 'dump.java', 'w') as source_file:
            source_file.write(source_code)
            source_file.close()
        cmd = 'javac ' + settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id + 'dump.java '
        print("CMD> ", cmd)

        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = child.communicate()
        error = error.decode()
        if not error == '':
            return CompileStatus(False, error)
        else:
            return CompileStatus(True, 'compile succeeded.')

    def execute(self, input_data) -> ExecutionStatus:
        """
        Method used to execute the given program with the given data.
        :param input_data: input data for the algorithm.
        """
        formatted_input = self._formatter.format_from_dict(input_data)

        compile_files = os.listdir(settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id)
        compile_files.remove('dump.java')
        cmd = 'java -classpath ' + settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id + ' ' + \
              compile_files[0].split('.')[0] + ' ' + formatted_input
        print("CMD> ", cmd)

        return self._run_process(cmd)


class PythonExecutor(Executor):
    """
    Specific executor for Python programs.
    """

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self.__unique_id = "-1"

    def set_unique_id(self, id_):
        """
        Set the unique ID for the task.
        :param id_: The ID to be set.
        """
        self.__unique_id = id_

    def compile(self, source_code):
        """
        Method used to compile the given program.
        :param source_code: The source code for the program.
        :return: returns a compile status object
        """
        if not os.path.exists(settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id):
            os.mkdir(settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id)
        with open(settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id + 'dump.py', 'w') as source_file:
            source_file.write(source_code)
            source_file.close()
        return CompileStatus(True, '')

    def execute(self, input_data):
        """
        Method used to execute the given program with the given data.
        :param input_data: input data for the algorithm.
        """

        formatted_input = self._formatter.format_from_dict(input_data)

        cmd = 'python ' + settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id + 'dump.py ' + formatted_input
        return self._run_process(cmd)


class ExecutionController(object):
    """
    Controller class for all different kinds of specific executors.
    """

    def __init__(self, language):
        """
        Controller.
        :param language: the required language
        """
        self._language = language
        self.__temp_file_id = -1
        self.__compile_status = CompileStatus(None, None)
        if self._language == 'java':
            self._executor = JavaExecution()
        elif self._language == 'python':
            self._executor = PythonExecutor()

    def compile(self, source_code) -> CompileStatus:
        """
        Method used to compile the given program.
        :param source_code: The source code for the program.
        :return: returns a compile status object
        """
        self._executor.set_unique_id(self.__generate_unique_id(source_code))
        self.__compile_status = self._executor.compile(source_code=source_code)
        return self.__compile_status

    def execute(self, input_data) -> ExecutionStatus:
        """
        Method used to execute the given program with the given data.
        :param input_data: input data for the algorithm.
        """
        if self.__compile_status.status is True:
            execution_status = self._executor.execute(input_data=input_data)
            return execution_status
        else:
            return ExecutionStatus(False, 'Compile failed', 'None', -1)

    def __generate_unique_id(self, source_code):
        """
        Generate a unique ID  for the current task based on the source code.
        :param source_code: teh source code of the program.
        :return: returns a unique ID.
        """
        return str(hash(source_code)) + '/'
