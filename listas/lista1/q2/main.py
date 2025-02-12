from models.nome import Nome
from models.idade import Idade

nome  = Nome ("Teofilo")
idade = Idade ('18')

print (nome.__dict__)
print(idade.__dict__)