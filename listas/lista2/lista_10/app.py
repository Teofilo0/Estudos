from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, make_response
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
    import sqlite3
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

        # Verificar a força da senha
        senha_criptografada = generate_password_hash(password)

        try:
            usuario = User(username=username, password=senha_criptografada, nome=nome)
            usuario.salvar()
            return redirect(url_for('login'))
        except ValueError as e:
            return render_template('cadastro.html', erro=str(e))
        
    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM usuarios WHERE username = ?''', (username,))
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
    
    usuarios = User.listar_todos()  # Agora esta linha está dentro do escopo correto.
    return render_template('usuarios.html', usuarios=usuarios)

# Rota para editar os dados do usuário logado
@app.route('/editar', methods=['GET', 'POST'])
def editar_usuario():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirecionar para o login se não estiver logado

    # Buscar o usuário logado
    usuario = User.buscar_por_username(username)
    if not usuario:
        return redirect(url_for('login'))  # Se o usuário não for encontrado, redireciona para o login

    if request.method == 'POST':
        # Receber os novos dados
        novo_nome = request.form['nome']
        nova_senha = request.form['password']

        # Verificar se a senha foi alterada
        if nova_senha:
            nova_senha_criptografada = generate_password_hash(nova_senha)
        else:
            nova_senha_criptografada = usuario['password']

        # Atualizar os dados no banco
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''UPDATE usuarios SET nome = ?, password = ? WHERE username = ?''',
                       (novo_nome, nova_senha_criptografada, username))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))  # Redirecionar para o dashboard após a edição

    return render_template('editar_usuario.html', usuario=usuario)

# Logout
@app.route('/logout', methods=['POST'])
def logout():
    # Remover usuário da sessão
    session.pop('username', None)
    # Remover o cookie
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0)  # Excluir o cookie
    return resposta