from flask import Flask, render_template, url_for, request, Blueprint, redirect
from books.models import Book
from users.models import User
from emprestimo.models import Emprestimos

bp = Blueprint('emprestimo', __name__, url_prefix='/emprestimo', template_folder='templates')

@bp.route('/')
def index():
    return render_template('emprestimo/index.html', emprestimo = Emprestimos.all())

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        book_id = request.form['book_id']
        user_id = request.form['user_id']

        emprestimo = Emprestimos(user_id, book_id)
        emprestimo.save()

        return redirect(url_for('emprestimo.index'))
    
    livros = Book.all()
    users = User.all()
    return render_template('emprestimo/register.html', users=users, livros=livros)
