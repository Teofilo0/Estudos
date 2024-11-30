from flask import Blueprint, render_template, request, redirect, url_for
from models.user import db, User

# Cria um Blueprint para controlar as rotas relacionadas aos usuários
user_controller = Blueprint('user_controller', __name__)

# Rota para listar todos os usuários
@user_controller.route('/')
def index():
    users = User.query.all()  # Consulta todos os usuários do banco
    return render_template('pages/index.html', users=users)

# Rota para criar um novo usuário
@user_controller.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        user = User(
            email=request.form['email'],
            senha=request.form['senha']
        )
        db.session.add(user)
        db.session.commit()  # Confirma a adição do novo usuário
        return redirect(url_for('user_controller.index'))  # Redireciona para a lista de usuários

    return render_template('pages/create.html')

# Rota para editar um usuário existente
@user_controller.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):
    user = User.query.get(id)  # Busca o usuário pelo ID
    if not user:
        return redirect(url_for('error', message='Usuário não encontrado'))

    if request.method == 'POST':
        user.email = request.form['email']  # Atualiza o email do usuário
        db.session.commit()  # Confirma a alteração
        return redirect(url_for('user_controller.index'))

    return render_template('pages/edit.html', user=user)
