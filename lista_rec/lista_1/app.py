from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Bem-vindo ao Flask!"


@app.route('/sobre')
def sobre():
    return "Lorem"


@app.route('/saudacao/<nome>')
def sudacao(nome):
    return (f'Ola {nome} seja Bem vindo')
    


@app.route('/contato/<nome>/<numero>')
def contato(nome, numero):
    return (f'Ola {nome} seu numero de contanto é {numero}')
    