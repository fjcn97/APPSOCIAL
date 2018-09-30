from flask import Flask, g
from config import Config
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import os, logging
from myconnutils import getConnection
        
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Faça login para aceder a esta página.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.before_request
    def get_db():
        if 'db' not in g:
            g.db = getConnection()

    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    login_manager.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.tarefa import bp as tarefa_bp
    app.register_blueprint(tarefa_bp)

    from app.utente import bp as utente_bp
    app.register_blueprint(utente_bp)

    from app.equipa import bp as equipa_bp
    app.register_blueprint(equipa_bp)

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        #Regista os erros num ficheiro log
        file_handler = RotatingFileHandler('logs/APPSOCIAL.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('APPSOCIAL startup')
        
    return app

from app import models
