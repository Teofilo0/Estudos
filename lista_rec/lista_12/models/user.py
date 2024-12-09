from flask_login import UserMixin
import sqlite3


def conectar_banco():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row  # Para acessar os resultados como dicionários
    return conn


class User(UserMixin):
    def __init__(self, username, password=None, nome=None, id=None):
        self.id = id
        self.username = username
        self.password = password
        self.nome = nome

    def salvar(self):
        conn = conectar_banco()
        cursor = conn.cursor()
        try:
            # Inserir o usuário no banco de dados (não passamos o id)
            cursor.execute('''
            INSERT INTO usuarios (username, password, nome)
            VALUES (?, ?, ?)
            ''', (self.username, self.password, self.nome))
            conn.commit()

            # Agora recuperamos o id gerado automaticamente
            self.id = cursor.lastrowid  # Atribui o id gerado ao objeto

        except Exception as e:
            raise ValueError(f"Erro ao salvar usuário: {e}")
        finally:
            conn.close()

    @staticmethod
    def buscar_por_username(username):
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, nome FROM usuarios WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(id=user[0], username=user[1], password=user[2], nome=user[3])
        return None

    @staticmethod
    def buscar_por_id(id):
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, nome FROM usuarios WHERE id = ?', (id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(id=user[0], username=user[1], password=user[2], nome=user[3])
        return None

    @staticmethod
    def listar_todos():
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, nome FROM usuarios')
        usuarios = cursor.fetchall()
        conn.close()
        return [User(id=user[0], username=user[1], password=user[2], nome=user[3]) for user in usuarios]
