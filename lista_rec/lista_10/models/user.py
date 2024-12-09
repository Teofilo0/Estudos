from database import conectar_banco



# Modelo User

class User:
    def __init__(self, username, password, nome):
        self.username = username
        self.password = password
        self.nome = nome

    @staticmethod
    def buscar_por_username(username):
        # Consultar o banco de dados para buscar o usuário pelo username
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM usuarios WHERE username = ?''', (username,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    def salvar(self):
        # Função de salvar o usuário no banco de dados
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO usuarios (username, password, nome) VALUES (?, ?, ?)''',
                       (self.username, self.password, self.nome))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_todos():
        # Lista todos os usuários
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM usuarios''')
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios
