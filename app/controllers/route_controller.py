"""

"""
import json
import os

import subprocess

import time
from flask import Flask as Application, render_template, request

from app import settings
from app.controllers.AlgorithmExecutor import Algorithm
from app.controllers.complexity_manager import ComplexityManager
from app.controllers.execution_controller import ExecutionController
from app.controllers.file_controller import AlgorithmRepository
from app.models.data_generators import RandomDataGenerator
from app.models.decorators.crossdomain import crossdomain
from app.utils.platform_specific import format_path


class RouteController(object):
    """

    """

    def __init__(self, app: Application):
        """

        :param app:
        """
        self._app = app
        self.__index()
        self.__execute()
        self.__complexity()
        self.__local_complexity()

    def __index(self):
        @self._app.route('/')
        def render():
            body = dict(result='OK',
                        status=dict(type='SUCCESS', message='Started'))
            response = self._app.response_class(
                response=json.dumps(body),
                status=200,
                mimetype='application/json'
            )
            return response

    def __execute(self):
        @self._app.route('/execute', methods=['POST'])
        def render_view():

            algorithm_name = request.form['algorithm']
            algorithm_input = json.loads(request.form['input'])

            algorithm = Algorithm(algorithm_name)
            if algorithm.validate_input(algorithm_input):
                path_, language = AlgorithmRepository.get_algorithm_path(algorithm_name)
                formatted_input = algorithm.get_formatted_input(algorithm_input)

                output = algorithm.execute(language, path_, formatted_input)

                body = dict(status=dict(execution_time=1000, type='SUCCESS', message='Entered'),
                            output=output.decode().strip())
            else:
                body = dict(status=dict(execution_time=1000, type='FAILED',
                                        message='Requested algorithm can not be executed with the given data'),
                            output="None")
            response = self._app.response_class(
                response=json.dumps(body),
                status=200,
                mimetype='application/json'
            )
            return response

    def __complexity(self):

        @self._app.route('/complexity', methods=['POST'])
        def render_complexity():
            language = request.form['language']
            source_code = request.form['source_code']
            parameters_meta_data = json.loads(request.form['parameters'])

            program = ExecutionController(language=language)
            compile_status = program.compile(source_code=source_code)
            if compile_status.status is False:
                body = dict(status=dict(execution_time=0, type='FAILED',
                                        message="Done"),
                            compile_status=compile_status)
                response = self._app.response_class(
                    response=json.dumps(body),
                    status=200,
                    mimetype='application/json'
                )
                return response

            complexity_manager = ComplexityManager(settings.MULTIPLY_FACTOR)
            data = RandomDataGenerator(parameters_meta_data, settings.AFFORDABLE_INT_LIMIT, settings.MULTIPLY_FACTOR)
            execution_result = "Failed"
            run_times = list()
            complexity_name = 'Undefined'
            while data.next():
                input_data = data.get_random_data()

                print('input data>', input_data)
                try:
                    execution_result = program.execute(input_data=input_data)
                except OSError:
                    break
                if execution_result is None:
                    complexity_name = complexity_manager.get_complexity(run_times[-2], run_times[-1])
                    break
                elif execution_result.run_time >= settings.RUN_TIME_LIMIT*1000:
                    run_times.append(execution_result.run_time)
                    complexity_name = complexity_manager.get_complexity(run_times[-2], run_times[-1])
                    break
                else:
                    run_times.append(execution_result.run_time)
            if complexity_name == 'Undefined':

                complexity_name = complexity_manager.get_complexity(run_times[-2], run_times[-1])
            body = dict(status=dict(execution_time=str(run_times), type='SUCCESS',
                                    message="Done"),
                        compile_status="Done",
                        execution_status=execution_result,
                        complexity=complexity_name)
            response = self._app.response_class(
                response=json.dumps(body),
                status=200,
                mimetype='application/json'
            )
            return response

    def __local_complexity(self):
        @self._app.route('/local_complexity', methods=['POST'])
        def render_comp_execution():
            algorithm_name = request.form['algorithm']
            algorithm = Algorithm(algorithm_name)
            path_, language = AlgorithmRepository.get_algorithm_path(algorithm_name)

            params = algorithm.get_parameter_model()
            for param in params:
                param['growth'] = "exponential"

            data = RandomDataGenerator(params, settings.AFFORDABLE_INT_LIMIT, settings.MULTIPLY_FACTOR)
            complexity_manager = ComplexityManager(settings.MULTIPLY_FACTOR)

            run_times = []
            while data.next():
                input_data = data.get_random_data()

                print(input_data)

                formatted_input = algorithm.get_formatted_input(input_data)
                output = algorithm.execute(language, path_, formatted_input)
                execution_time = int(output)
                print("executionR ", execution_time)
                if execution_time >= settings.RUN_TIME_LIMIT * 1000:
                    run_times.append(execution_time)
                run_times.append(execution_time)

            complexity_name = complexity_manager.get_complexity(run_times[-2], run_times[-1])
            body = dict(status=dict(type='SUCCESS',
                                    message="Done",
                                    complexity=str(complexity_name)))
            response = self._app.response_class(
                response=json.dumps(body),
                status=200,
                mimetype='application/json'
            )
            return response