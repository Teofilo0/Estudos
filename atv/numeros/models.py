from database import get_connection

class Numero:
    def __init__(self, numero,user_id ):
        self.numero = numero
        self.user_id = user_id
        
    def save(self):
        conn = get_connection()
        conn.execute("INSERT INTO numeros(numero,user_id) values(?,?)", (self.numero,self.user_id))
        conn.commit()
        conn.close()
        return True
    
    @classmethod
    def all(cls):
        conn = get_connection()
        numeros = conn.execute("SELECT * FROM numeros").fetchall()
        numeros.execute("""
            SELECT numeros.numero, numeros.user_id, users.nome 
            FROM numeros
            JOIN users ON numeros.user_id = users.id
        """)
        return numeros

