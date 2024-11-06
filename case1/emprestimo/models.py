from database import get_connection

class Emprestimos:
    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id

    def save(self):
        conn = get_connection()
        conn.execute("INSERT INTO emprestimo(book_id, user_id) values(?,?)", (self.book_id, self.user_id))
        conn.commit()
        conn.close()
        return True 


    @classmethod
    def all(cls):
        conn = get_connection()
        conect = """
            SELECT emprestimo.id, books.titulo, users.nome FROM emprestimo
            JOIN books ON emprestimo.book_id = books.id
            JOIN users ON emprestimo.user_id = users.id
            """
        emprestimos = conn.execute(conect).fetchall()
        return [
            {
                "id": i[0],
                "book_title": i[1],
                "user_name": i[2]
            }
            for i in emprestimos
        ]