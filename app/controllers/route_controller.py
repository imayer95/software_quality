"""
Module that stores all the routes exposed by the API.
"""

import json

from flask import Flask as Application, request

from app import settings
from app.controllers.algorithm_executor import Algorithm
from app.controllers.complexity_manager import ComplexityManager
from app.controllers.execution_controller import ExecutionController
from app.controllers.file_controller import AlgorithmRepository
from app.models.data_generators import RandomDataGenerator


class RouteController(object):
    """
    Controller class for the routes.
    """

    def __init__(self, app: Application):
        """
        Constructor.
        :param app: a flask Application object.
        """
        self._app = app
        self.__index()
        self.__execute()
        self.__complexity()
        self.__local_complexity()

    def __index(self):
        """
        Index route.
        forst entry point for the API.
        """

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
        """
        Execution route used to receive the algorithm name with input data and compiles and executes that program.
        """

        @self._app.route('/execute', methods=['POST'])
        def render_view():

            # Read the request data.
            algorithm_name = request.form['algorithm']
            algorithm_input = json.loads(request.form['input'])

            # Create the model for the algorithm and validate the given input.
            algorithm = Algorithm(algorithm_name)
            if algorithm.validate_input(algorithm_input):

                # Get the path to the stored algorithm and format the given input.
                path_, language = AlgorithmRepository.get_algorithm_path(algorithm_name)
                formatted_input = algorithm.get_formatted_input(algorithm_input)

                # Execute the stored algorithm
                output = algorithm.execute(language, path_, formatted_input)

                # Generate the corresponding response for the client.
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
        """
        Complexity route used to receive raw source code and the programming language and generates the complexity
        of the algorithm.
        """

        @self._app.route('/complexity', methods=['POST'])
        def render_complexity():

            # Read the request data.
            language = request.form['language']
            source_code = request.form['source_code']
            parameters_meta_data = json.loads(request.form['parameters'])

            # Create an execution controller class and compile the source code.
            program = ExecutionController(language=language)
            compile_status = program.compile(source_code=source_code)

            # If the compilation failed, return a response to the client to notify him.
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

            # While it has not reached the generation limit, keep execution the algorithm with exponential data.
            while data.next():
                input_data = data.get_random_data()

                print('input data>', input_data)
                try:
                    execution_result = program.execute(input_data=input_data)
                except OSError:
                    break

                # If the execution result returned is None, calculate the complexity and stop the random data generation
                if execution_result is None:
                    complexity_name = complexity_manager.get_complexity(run_times[-2], run_times[-1])
                    break

                # If the last execution time is larger than the imposed limit,
                elif execution_result.run_time >= settings.RUN_TIME_LIMIT * 1000:
                    run_times.append(execution_result.run_time)
                    complexity_name = complexity_manager.get_complexity(run_times[-2], run_times[-1])
                    break

                # else append the last execution time.
                else:
                    run_times.append(execution_result.run_time)

            # if the complexity name remained undefined after the while cycle, compute it using
            # the last 2 execution times
            if complexity_name == 'Undefined':
                complexity_name = complexity_manager.get_complexity(run_times[-2], run_times[-1])

            # generate the response and respond to the client.
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
        """
        Route used to compute the complexity of the stored algorithms.
        """

        @self._app.route('/local_complexity', methods=['POST'])
        def render_comp_execution():

            # Read data from request.
            algorithm_name = request.form['algorithm']

            # Create the algorithm model and retrieve the path and language for the algorithm
            algorithm = Algorithm(algorithm_name)
            path_, language = AlgorithmRepository.get_algorithm_path(algorithm_name)

            params = algorithm.get_parameter_model()
            for param in params:
                param['growth'] = "exponential"

            data = RandomDataGenerator(params, settings.AFFORDABLE_INT_LIMIT, settings.MULTIPLY_FACTOR)
            complexity_manager = ComplexityManager(settings.MULTIPLY_FACTOR)

            run_times = []

            # while there is still new random data to be generated, keep execution the algorithm with exponential data.
            while data.next():
                input_data = data.get_random_data()

                print(input_data)

                # using the net input data, format it, and execute the algorithm.
                formatted_input = algorithm.get_formatted_input(input_data)
                output = algorithm.execute(language, path_, formatted_input)
                execution_time = int(output)

                # if the last execution time is larger then the imposed limit, store the last generated execution time.
                if execution_time >= settings.RUN_TIME_LIMIT * 1000:
                    run_times.append(execution_time)
                run_times.append(execution_time)

            # compute the complexity by using the last two execution times.
            complexity_name = complexity_manager.get_complexity(run_times[-2], run_times[-1])

            # create the response for the client.
            body = dict(status=dict(type='SUCCESS',
                                    message="Done",
                                    complexity=str(complexity_name)))
            response = self._app.response_class(
                response=json.dumps(body),
                status=200,
                mimetype='application/json'
            )
            return response
