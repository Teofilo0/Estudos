from flask import Flask, render_template, url_for, request,Blueprint,redirect
from users.models import User


bp = Blueprint('users', __name__, url_prefix='/users', template_folder='templates')

@bp.route('/')
def index():
    return render_template('users/index.html', users = User.all())

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_id = request.form['nome']

        users = User(user_id)
        users.save()

        return redirect(url_for('users.index'))
    
    users = User.all()
    return render_template('users/register.html', users=users)

