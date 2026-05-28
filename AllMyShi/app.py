from flask import Flask
from routes.main import main_bp
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)

    #Configuartion
    app.config['SECRET_KEY'] =  'your-secret-key'
    app.config['DATABASE'] = 'database/users.db'
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True) 