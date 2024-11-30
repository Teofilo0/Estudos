from flask import Flask, request, render_template, \
    redirect, url_for, flash
import sqlite3, os.path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String,text
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


app = Flask(__name__)

# habilitar mensagens flash
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'muitodificil'


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    senha: Mapped[str]


db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = db.session.execute(db.select(User).order_by(User.email)).scalars()

    return render_template('pages/index.html', users=users)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        user = User(
            email=request.form["email"],
            senha=request.form["senha"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index", id=user.id))

    
    return render_template('pages/create.html')

@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):

    # obter informação do usuário
    user = db.session.execute(text('SELECT id, email, senha FROM users WHERE id = :id'), {'id': id}).fetchone()

    if user is None:
        return redirect(url_for('error', message='Usuário Inexistente'))

    if request.method == 'POST':
        email = request.form['email']
        db.session.execute(text('UPDATE users SET email=:email WHERE id=:id'),{'email': email, 'id': id})
        db.session.commit() 

        return redirect(url_for('index'))
    
    return render_template('pages/edit.html', user=user)
