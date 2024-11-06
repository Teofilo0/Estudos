from flask import Flask
from controllers import users, books,emprestimo

app = Flask(__name__)
app.register_blueprint(users.bp)
app.register_blueprint(books.bp)
app.register_blueprint(emprestimo.bp)