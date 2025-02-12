import sqlite3
DATABASE = 'usuarios.db'

def conectar_banco():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Configura para retornar linhas como dicionários
    return conn

def criar_tabela():
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        # Criação das tabelas, se ainda não existirem
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT UNIQUE,
                          password TEXT,
                          nome TEXT)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS receitas (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          title TEXT,
                          description TEXT,
                          user_id INTEGER,
                          FOREIGN KEY (user_id) REFERENCES usuarios(id))''')
        
        conn.commit()
        conn.close()
# Inicializa o banco de dados ao iniciar a aplicação
    criar_tabela()
