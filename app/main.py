"""
Server entry point.
"""

from flask import Flask

from app.controllers.route_controller import RouteController

if __name__ == '__main__':
    app = Flask(__name__)

    RouteController(app=app)
    app.run(host='0.0.0.0', port=8000, threaded=True)
