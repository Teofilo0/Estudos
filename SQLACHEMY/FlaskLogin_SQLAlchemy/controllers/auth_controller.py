from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.User import User
from models.Livro import Livro
from database import db

auth = Blueprint("auth", __name__)

@auth.route('/')
def index():
    users = db.session.execute(db.select(User).order_by(User.nome)).scalars().all()
    livros = db.session.execute(db.select(Livro).order_by(Livro.titulo)).scalars().all()
    return render_template("index.html", users=users, livros=livros)

@auth.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = User(nome=nome)
        user.set_password(senha)  # Define a senha usando o método set_password
        db.session.add(user)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for("auth.login"))

    return render_template("registrar_usuario.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = User.query.filter_by(nome=nome).first()
        if user and user.check_password(senha):
            login_user(user)
            return redirect(url_for('auth.cadastrar_livro_usuario'))
        else:
            flash('Usuário ou senha incorretos.')
    return render_template('login.html')

@auth.route('/cadastrar_livro_usuario', methods=["GET", "POST"])
@login_required
def cadastrar_livro_usuario():
    if request.method == "POST":
        user_id = request.form["user_id"]
        titulo = request.form["titulo"]
        livro = Livro(titulo=titulo, user_id=user_id)
        db.session.add(livro)
        db.session.commit()
        flash('Livro cadastrado com sucesso!', 'success')
        return redirect(url_for("auth.index"))

    users = User.query.all()
    return render_template("registrar_livro_usuario.html", users=users)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))
