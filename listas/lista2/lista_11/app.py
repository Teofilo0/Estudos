from models import User, Recipe
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, make_response
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'chave-secreta'

# Função para verificar a força da senha
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

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['password'], password):
            session['username'] = username
            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age=60*60*24)
            return resposta
        return render_template('login.html', erro='Usuário ou senha inválidos.')

    if 'username' in session:
        return redirect(url_for('dashboard'))

    return render_template('login.html')


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
            nova_senha_criptografada = usuario['password']

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET nome = ?, password = ? WHERE username = ?',
                       (novo_nome, nova_senha_criptografada, username))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('editar_usuario.html', usuario=usuario)


# Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0)
    return resposta


# Rota para listar e adicionar receitas
@app.route('/receitas', methods=['GET', 'POST'])
def receitas():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM usuarios WHERE username = ?', (session['username'],))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return redirect(url_for('login'))

    user_id = user[0]

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        try:
            receita = Recipe(title=title, description=description, user_id=user_id)
            receita.salvar()
            return redirect(url_for('receitas'))
        except ValueError as e:
            return render_template('receitas.html', erro=str(e), receitas=Recipe.listar_por_usuario(user_id))

    receitas = Recipe.listar_por_usuario(user_id)
    return render_template('receitas.html', receitas=receitas)


# Rota para editar uma receita
@app.route('/editar_receita/<int:id>', methods=['GET', 'POST'])
def editar_receita(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM receitas WHERE id = ?', (id,))
    receita = cursor.fetchone()
    conn.close()

    if not receita:
        return redirect(url_for('receitas'))

    if request.method == 'POST':
        novo_titulo = request.form['title']
        nova_descricao = request.form['description']

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('UPDATE receitas SET title = ?, description = ? WHERE id = ?',
                       (novo_titulo, nova_descricao, id))
        conn.commit()
        conn.close()

        return redirect(url_for('receitas'))

    return render_template('editar_receita.html', receita=receita)


# Rota para excluir uma receita
@app.route('/excluir_receita/<int:id>', methods=['POST'])
def excluir_receita(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM receitas WHERE id = ?', (id,))
    conn.commit()
    conn.close()

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
