from flask import Flask, render_template, request, redirect, url_for, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Recipe
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
import sqlite3
import re
import time
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'chave-secreta'


login_manager = LoginManager()
login_manager.init_app(app) 


app.permanent_session_lifetime = timedelta(minutes=5)


def verificar_forca_senha(senha):
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."
    if not re.search(r"[A-Z]", senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    return True, ""

def conectar_banco():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def verificar_inatividade():
    if 'last_activity' in session:
        tempo_inatividade = time.time() - session['last_activity']
        if tempo_inatividade > 300: 
            session.pop('username', None)
            return redirect(url_for('login'))
    session['last_activity'] = time.time() 


@login_manager.user_loader
def load_user(user_id):
    return User.buscar_por_id(user_id)

# Rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']

        senha_criptografada = generate_password_hash(password)

        try:
            usuario = User(username=username, password=senha_criptografada, nome=nome)
            usuario.salvar()
            return redirect(url_for('login'))
        except ValueError as e:
            return render_template('cadastro.html', erro=str(e))

    return render_template('cadastro.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.buscar_por_username(username)

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('receitas'))
        else:
            return render_template('login.html', erro="Usuário ou senha inválidos.")
    return render_template('login.html')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rota do dashboard
@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=username)

# Rota para listar usuários
@app.route('/usuarios')
def listar_usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))

    usuarios = User.listar_todos()
    return render_template('usuarios.html', usuarios=usuarios)

# Rota para editar os dados do usuário logado
@app.route('/editar', methods=['GET', 'POST'])
def editar_usuario():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    usuario = User.buscar_por_username(username)
    if not usuario:
        return redirect(url_for('login'))

    if request.method == 'POST':
        novo_nome = request.form['nome']
        nova_senha = request.form['password']

        if nova_senha:
            nova_senha_criptografada = generate_password_hash(nova_senha)
        else:
            nova_senha_criptografada = usuario.password

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET nome = ?, password = ? WHERE username = ?',
                       (novo_nome, nova_senha_criptografada, username))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('editar_usuario.html', usuario=usuario)

# Rota para receitas
@app.route('/receitas', methods=['GET', 'POST'])
@login_required
def receitas():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        try:
            receita = Recipe(title=title, description=description, user_id=current_user.id)
            receita.salvar()
            return redirect(url_for('receitas'))
        except ValueError as e:
            return render_template('receitas.html', erro=str(e), receitas=Recipe.listar_por_usuario(current_user.id))

    receitas = Recipe.listar_por_usuario(current_user.id)
    return render_template('receitas.html', receitas=receitas)

# Rota para editar uma receita
@app.route('/editar_receita/<int:id>', methods=['GET', 'POST'])
def editar_receita(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    # Buscar a receita pelo ID
    receita = Recipe.buscar_por_id(id)
    if not receita:
        return redirect(url_for('receitas'))

    if request.method == 'POST':
        novo_titulo = request.form['title']
        nova_descricao = request.form['description']
        
        # Atualizar a receita
        receita.title = novo_titulo
        receita.description = nova_descricao
        receita.salvar()

        return redirect(url_for('receitas'))

    return render_template('editar_receita.html', receita=receita)

# Rota para excluir uma receita
@app.route('/excluir_receita/<int:id>', methods=['POST'])
def excluir_receita(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    receita = Recipe.buscar_por_id(id)
    if receita:
        receita.excluir()

    return redirect(url_for('receitas'))

# Rota para buscar receitas por título
@app.route('/buscar_receitas', methods=['GET', 'POST'])
def buscar_receitas():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo_busca = request.form['title']
        receitas = Recipe.buscar_por_titulo(titulo_busca)
        return render_template('receitas.html', receitas=receitas)

    return render_template('buscar_receitas.html')
