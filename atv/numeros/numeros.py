from flask import Flask, render_template, url_for, request,Blueprint,redirect
from users.models import User
from numeros.models import Numero

bp = Blueprint('numeros', __name__, url_prefix='/numeros', template_folder='templates')

@bp.route('/')
def index():
    return render_template('numeros/index.html', numeros = Numero.all())

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        numero_id = request.form['numero']
        user_id = request.form['user_id']

        numeros = Numero(numero_id,user_id)
        numeros.save()

        return redirect(url_for('numeros.index'))
    
    numeros = Numero.all()
    users = User.all()
    return render_template('numeros/register.html', numeros=numeros,users=users)

