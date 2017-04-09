"""

"""
import json
import os

import subprocess
from flask import Flask as Application


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
            return response

    def __execute(self):
        @self._app.route('/execute/<algo>/<input_>', methods=['GET', 'POST'])
        def render_view(algo, input_):
            path_ = os.getcwd() + '\\res\python\\' + algo + '.py'
            formatted_input = ''
            for arg in input_.split(','):
                formatted_input += arg + ' '
            child = subprocess.Popen('python ' + path_ + ' ' + formatted_input, shell=True, stdout=subprocess.PIPE)
            output = child.communicate()[0]
            body = dict(status=dict(execution_time=1000, type='SUCCESS', message='Entered'),
                        output=output.decode().strip())

            response = self._app.response_class(
                response=json.dumps(body),
                status=200,
                mimetype='application/json'
            )
            return response
