"""

"""
import json
import os

import subprocess
from flask import Flask as Application, render_template, request

from app.controllers.file_controller import AlgorithmRepository
from app.models.input_processor import Algorithm
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
        self.__test()

    def __index(self):
        @self._app.route('/')
        def render():
            body = dict(result='OK',
                        status=dict(type='SUCCESS', message='Entered'))
            response = self._app.response_class(
                response=json.dumps(body),
                status=200,
                mimetype='application/json'
            )

            ar = AlgorithmRepository()
            ar.get_algorithm_path('test1')

            return response

    def __execute(self):
        @self._app.route('/execute', methods=['GET', 'POST'])
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

    def __test(self):
        @self._app.route('/test', methods=['POST'])
        def __test():
            print('here')
            data = request.form['data']
            print('DATA: ', data)
            body = dict(result='OK',
                        status=dict(type='SUCCESS', message='Entered'))
            response = self._app.response_class(
                response=json.dumps(body),
                status=200,
                mimetype='application/json'
            )
            return response