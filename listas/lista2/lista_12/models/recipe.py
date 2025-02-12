import sqlite3


def conectar_banco():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row  

class Recipe:
    def __init__(self, title, description, user_id, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id

    def salvar(self):
        conn = conectar_banco()
        cursor = conn.cursor()
        if self.id:
          
            cursor.execute('''UPDATE receitas SET title = ?, description = ? WHERE id = ?''',
                           (self.title, self.description, self.id))
        else:
            
            cursor.execute('''INSERT INTO receitas (title, description, user_id)
                              VALUES (?, ?, ?)''', (self.title, self.description, self.user_id))
        conn.commit()
        conn.close()

    def excluir(self):
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM receitas WHERE id = ?''', (self.id,))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_por_usuario(user_id):
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM receitas WHERE user_id = ?', (user_id,))
        receitas = cursor.fetchall() 
        conn.close()
        
 
        return [Recipe(id=row['id'], title=row['title'], description=row['description'], user_id=row['user_id']) for row in receitas]

    @staticmethod
    def buscar_por_titulo(titulo):
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM receitas WHERE title LIKE ?', ('%' + titulo + '%',))
        receitas = cursor.fetchall()
        conn.close()
        

        return [Recipe(id=row['id'], title=row['title'], description=row['description'], user_id=row['user_id']) for row in receitas]
