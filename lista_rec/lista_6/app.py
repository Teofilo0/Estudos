from flask import Flask, request, render_template, session, redirect,url_for, make_response,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.secret_key = 'chave-secreta'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)


class User(db.Model):
    __tablename__  = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] =  mapped_column(unique=True)
    password: Mapped[str]


with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user =User(
            username = request.form['username'],
            password = request.form['password'],
        )
        existing_user = User.query.filter_by(username=user.username).first()

        if existing_user:
            flash('Usuário já existente')
            return redirect(url_for('login'))

        # Usuário e senha pré-definidos
        db.session.add(user)
        db.session.commit()


        resposta = make_response(redirect(url_for('dashboard')))
        resposta.set_cookie('username', user.username, max_age=60*60*24) 
        return render_template('dashboard.html')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Verificar se o usuário está na sessão
    username = session.get('username')
    if not username:
        return redirect(url_for('login')) # Redirecionar para o login se não estiver logado
    
    return render_template('dashboard.html', username=username)


@app.route('/logout', methods=['POST'])
def logout():
    
    # Remover usuário da sessão
    session.pop('username', None)

    # Remover o cookie 
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', expires=0)  # Excluir o cookie


    return resposta