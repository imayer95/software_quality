"""
module that handles the subprocess calls of the system
"""
import os
import subprocess
from subprocess import check_output, STDOUT

import time

from app import settings
from app.models.input_processor import InputFormatter
from app.models.threads import TimeOutThread


class CompileStatus(dict):
    def __init__(self, status, message, **kwargs):
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
    def __init__(self, status, message, result, run_time):
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
    def __init__(self):
        self._formatter = InputFormatter()

    def compile(self, source_code) -> CompileStatus:
        pass

    def execute(self, input_data) -> ExecutionStatus:
        pass

    def set_unique_id(self, id_):
        pass


class JavaExecution(Executor):

    def __init__(self):
        super().__init__()
        self.__unique_id = -1

    def set_unique_id(self, id_):
        self.__unique_id = id_

    def compile(self, source_code) -> CompileStatus:
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
        formatted_input = self._formatter.format_from_dict(input_data)

        compile_files = os.listdir(settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id)
        compile_files.remove('dump.java')
        cmd = 'java -classpath ' + settings.TEMP_COMPILATION_DIRECTORY + self.__unique_id + ' ' + \
              compile_files[0].split('.')[0] + ' ' + formatted_input
        print("CMD> ", cmd)

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
                                   error.replace('\r', '').replace('\n', '').replace('\t', ''), int(end-start))
        else:
            return ExecutionStatus(True, 'Execution done',
                                   output.replace('\r', '').replace('\n', '').replace('\t', ''), int(end-start))


class PythonExecutor(Executor):
    def __init__(self):
        super().__init__()
        self._unique_id = -1

    def set_unique_id(self, id_):
        pass

    def compile(self, source_code):
        return False

    def execute(self, input_data):
        return False


class ExecutionController(object):
    """
    
    """

    def __init__(self, language):
        self._language = language
        self.__temp_file_id = -1
        self.__compile_status = CompileStatus(None, None)
        if self._language == 'java':
            self._executor = JavaExecution()
        elif self._language == 'python':
            self._executor = PythonExecutor()

    def compile(self, source_code) -> CompileStatus:
        self._executor.set_unique_id(self.__generate_unique_id(source_code))
        self.__compile_status = self._executor.compile(source_code=source_code)
        return self.__compile_status

    def execute(self, input_data) -> ExecutionStatus:
        if self.__compile_status.status is True:
            execution_status = self._executor.execute(input_data=input_data)
            return execution_status
        else:
            return ExecutionStatus(False, 'Compile failed', 'None', -1)

    def __generate_unique_id(self, source_code):
        return str(hash(source_code)) + '\\'


