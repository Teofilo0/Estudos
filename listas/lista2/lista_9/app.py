from flask import Flask, request, render_template, session, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'chave-secreta'
DATABASE = 'usuarios.db'

def conectar_banco():
    return sqlite3.connect(DATABASE)

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        nome TEXT NOT NULL)''')
    conn.commit()
    conn.close()


criar_tabela()


def validar_senha(senha):
    if len(senha) < 8:
        return "A senha deve ter pelo menos 8 caracteres."
    if not re.search("[A-Z]", senha):
        return "A senha deve conter pelo menos uma letra maiúscula."
    return None

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']


        erro_senha = validar_senha(password)
        if erro_senha:
            return render_template('cadastro.html', erro=erro_senha)

        senha_hash = generate_password_hash(password)

        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO usuarios (username, password, nome)
                            VALUES (?, ?, ?)''', (username, senha_hash, nome))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('cadastro.html', erro='Usuário já cadastrado.')

    return render_template('cadastro.html')

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

        if usuario and check_password_hash(usuario[2], password):
            session['username'] = username
            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age=60*60*24)
            return resposta
        return render_template('login.html', erro='Usuário ou senha inválidos.')

    if 'username' in session:
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0)  # Excluir o cookie
    return resposta

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redireciona para login se não estiver logado
    username = session['username']
    return render_template('dashboard.html', username=username)

@app.route('/redefinir_senha', methods=['GET', 'POST'])
def redefinir_senha():
    if request.method == 'POST':
        username = request.form['username']
        nova_senha = request.form['nova_senha']
        confirmar_senha = request.form['confirmar_senha']

        # Validação da senha
        erro_senha = validar_senha(nova_senha)
        if erro_senha:
            return render_template('redefinir_senha.html', erro=erro_senha)

        if nova_senha != confirmar_senha:
            return render_template('redefinir_senha.html', erro='As senhas não coincidem.')

        # Hashing da nova senha
        senha_hash = generate_password_hash(nova_senha)

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''UPDATE usuarios SET password = ? WHERE username = ?''', (senha_hash, username))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('redefinir_senha.html')

@app.route('/usuarios')
def listar_usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT nome, username FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios)
