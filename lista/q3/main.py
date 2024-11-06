from models.nome import Nome
from models.idade import Idade
from models.curso import Curso
from database import create_db, get_connection, save


create_db('teste.db', 'sqlite.sql')    
create_db('novo.db', 'sqlite.sql')

n = Nome('João')
save(n, 'novo.db')

i = Idade('18')
save(i, 'novo.db')

c = Curso ('Informatica')
save (c, 'novo.db')