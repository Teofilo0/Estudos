from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
from models.User import User
from models.Livro import Livro
from controllers.auth_controller import auth
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///teste.db"
app.config["SECRET_KEY"] = "sua_chave_secreta_aqui"

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

with app.app_context():
    db.create_all()

# Registre o Blueprint
app.register_blueprint(auth)