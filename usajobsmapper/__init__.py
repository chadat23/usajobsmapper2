import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=True)

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


# if (-not (Test-Path env:FLASK_APP )) { $env:FLASK_APP  = 'usajobsmapper' }
# if (-not (Test-Path env:FLASK_ENV )) { $env:FLASK_ENV  = 'development' }
