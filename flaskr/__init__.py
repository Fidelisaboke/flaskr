import os 

from flask import Flask

def create_app(test_config=None):
    """The app factory function."""

    # Create Flask instance
    app = Flask(__name__, instance_relative_config=True)

    # Set up default configuration for the app
    # SECRET_KEY -> 'dev' for development but should be overriden in deployment.
    # DATABASE -> SQLite database path (app.instance_path => instance folder path).
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # A simple route to a page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Register the database functions
    from . import db
    db.init_app(app)

    # Register the auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)
        
    return app