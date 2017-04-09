"""
Server entry point.
"""

from flask import Flask

from src.controllers.route_controller import RouteController

if __name__ == '__main__':
    app = Flask(__name__)

    RouteController(app=app)

    app.run(host='127.0.0.1', port=8000, threaded=True)
