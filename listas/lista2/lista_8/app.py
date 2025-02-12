from flask import Flask, request, render_template, session, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'chave-secreta'  # Necessário para usar sessões no Flask

DATABASE = 'usuarios.db'

def conectar_banco():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Configura para retornar linhas como dicionários
    return conn


def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nome TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao iniciar a aplicação
criar_tabela()

# Função para verificar a força da senha
def verificar_forca_senha(senha):
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."
    if not re.search(r"[A-Z]", senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    return True, ""

# Rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']

        # Verificar a força da senha
        senha_forte, mensagem_erro = verificar_forca_senha(password)
        if not senha_forte:
            return render_template('cadastro.html', erro=mensagem_erro)

        # Hash da senha antes de armazenar
        password_hash = generate_password_hash(password)

        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO usuarios (username, password, nome)
            VALUES (?, ?, ?)
            ''', (username, password_hash, nome))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('cadastro.html', erro='Usuário já cadastrado.')
    return render_template('cadastro.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM usuarios WHERE username = ?
        ''', (username,))
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
        return redirect(url_for('login'))  # Redirecionar para o login se não estiver logado
    return render_template('dashboard.html', username=username)

# Rota para listar usuários
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

@app.route('/logout', methods=['POST'])
def logout():
    # Remover usuário da sessão
    session.pop('username', None)
    # Remover o cookie
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0)  # Excluir o cookie
    return resposta

if __name__ == '__main__':
    app.run(debug=True)
