from flask import Flask
from models.user import db
from controllers.usercontroller import user_controller


app = Flask(__name__, template_folder='templates')

# Configurações do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Desabilita o rastreamento de modificações

# Inicializa o banco de dados com a app
db.init_app(app)

# Registra o Blueprint de usuários


app.register_blueprint(user_controller, url_prefix='/users')

# Cria as tabelas do banco de dados, se necessário
with app.app_context():
    db.create_all()
