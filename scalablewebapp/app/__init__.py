#app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'authentication.do_the_login'
login_manager.session_protection = 'strong'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()




def create_app(config_type):    #dev,prod,test
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')
    app.config.from_pyfile(configuration)

#   Initialization
    db.init_app(app)    #bind database to flask app
    bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.catelog import main    #importing main blueprint
    app.register_blueprint(main)    #registering main blueprint

    from app.auth import authentication     #importing authentication blueprint
    app.register_blueprint(authentication)  #registering authentication blueprint

    return app
