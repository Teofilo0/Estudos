from database import conectar_banco


class Recipe:
    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id

    def salvar(self):
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO receitas (title, description, user_id) 
            VALUES (?, ?, ?)
        ''', (self.title, self.description, self.user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_por_usuario(user_id):
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM receitas WHERE user_id = ?', (user_id,))
        receitas = cursor.fetchall()
        conn.close()
        return receitas

    @staticmethod
    def buscar_por_titulo(titulo):
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM receitas WHERE title LIKE ?', ('%' + titulo + '%',))
        receitas = cursor.fetchall()
        conn.close()
        return receitas
