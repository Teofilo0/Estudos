import sqlite3
DATABASE = 'usuarios.db'

def conectar_banco():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Configura para retornar linhas como dicionários
    return conn

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    # Tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nome TEXT NOT NULL)
    ''')
    
    # Tabela de receitas (corrigindo para 'receitas' ou 'recipes')
    cursor.execute('''CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES usuarios(id))
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao iniciar a aplicação
criar_tabela()
