"""

"""
import json
import os

import subprocess
from flask import Flask as Application, render_template, request

from app.controllers.file_controller import AlgorithmRepository
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
        @self._app.route('/execute/<algo>/<input_>', methods=['GET', 'POST'])
        def render_view(algo, input_):
            path_ = AlgorithmRepository.get_algorithm_path(algo)

            formatted_input = ''
            for arg in input_.split(','):
                formatted_input += arg + ' '

            cmd = 'python ' + path_ + ' ' + formatted_input
            print("CMD> ", cmd)

            child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = child.communicate()[0]
            body = dict(status=dict(execution_time=1000, type='SUCCESS', message='Entered'),
                        output=output.decode().strip())

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