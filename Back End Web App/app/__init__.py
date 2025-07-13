from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Register blueprints
    from .routes import api
    app.register_blueprint(api)
    
    return app

app = create_app()