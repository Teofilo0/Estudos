import sqlite3
from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'chave-secreta'


def get_db():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row 
    return conn


def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        nome TEXT NOT NULL,
                        funcao TEXT)''')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']
        funcao = request.form.get('funcao', 'usuario')


        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        usuario = cursor.fetchone()
        if usuario:
            return render_template('cadastro.html', erro='Usuário já cadastrado.')


        conn.execute('INSERT INTO usuarios (username, password, nome, funcao) VALUES (?, ?, ?, ?)', 
                     (username, password, nome, funcao))
        conn.commit()
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))
        usuario = cursor.fetchone()
        
        if usuario:
            session['username'] = username
            session['funcao'] = usuario['funcao']
            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age=60*60*24)
            return resposta
        return render_template('login.html', erro='Usuário ou senha inválidos.')
    
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=username)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('funcao', None) 
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0)
    return resposta


@app.route('/usuarios')
def listar_usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))

    funcao_usuario = session.get('funcao')
    
    conn = get_db()
    cursor = conn.cursor()
    

    cursor.execute('SELECT username, nome, funcao FROM usuarios WHERE funcao = ?', (funcao_usuario,))
    usuarios = cursor.fetchall()
    
    return render_template('usuarios.html', usuarios=usuarios)

init_db()

