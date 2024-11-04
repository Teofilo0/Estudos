from flask import Flask, render_template, url_for, request, Blueprint, redirect
from models.user import User
from models.book import Book
from models.emprestimos import Emprestimos

bp = Blueprint('emprestimo', __name__, url_prefix='/emprestimo')

@bp.route('/')
def index():
    return render_template('emprestimo/index.html', emprestimo = Emprestimos.all())

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form['data']
        user = request.form['user']
        book = request.form['book']

        emprestimo = Emprestimos(data, user, book)
        emprestimo.save()
        return redirect(url_for('emprestimo.index'))


    return render_template('emprestimo/register.html', users=User.all(), books=Book.all())