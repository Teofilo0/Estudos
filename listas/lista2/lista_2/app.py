from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return "lorem"


@app.route('/perfil/<nome>')
def perfil(nome):
    if nome.lower() == "anonimo":
        return redirect(url_for('home'))
    return (f'Ola, {nome} Bem vindo')



