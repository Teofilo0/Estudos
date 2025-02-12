from database import get_connection

class Emprestimos:
    def __init__(self, data, user,book):
        self.data = data
        self.user_id = user
        self.book_id = book

    def save(self):
        conn = get_connection()
        conn.execute("INSERT INTO emprestimo(data, user_id,book_id) values(?,?,?)", (self.data, self.user_id, self.book_id))
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