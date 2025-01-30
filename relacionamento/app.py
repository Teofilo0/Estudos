from flask import Flask, render_template, request, redirect, url_for
from models import Manager, User
from flask_sqlalchemy import SQLAlchemy
from databse import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


db.init_app(app)
with app.app_context():
    db.create_all()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_manager', methods=['GET', 'POST'])
def register_manager():
    if request.method == 'POST':
        name = request.form['name']
        new_manager = Manager(name=name)
        db.session.add(new_manager)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register_manager.html')

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        manager_id = request.form['manager_id']
        new_user = User(name=name, manager_id=manager_id)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    managers = Manager.query.all()
    return render_template('register_user.html', managers=managers)

@app.route('/list_users')
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)


