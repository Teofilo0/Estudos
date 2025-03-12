from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'

Base = declarative_base()
engine = create_engine('sqlite:///site.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(Base, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    posts = relationship("Post", back_populates="author")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="posts")

Base.metadata.create_all(engine)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

@app.route('/')
def index():
    posts = session.query(Post).all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if len(name) < 3:
            flash('Nome deve ter pelo menos 3 caracteres.', 'danger')
        elif not email or '@' not in email:
            flash('Email inválido.', 'danger')
        elif len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'danger')
        elif password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
        else:
            user = User(name=name, email=email)
            user.set_password(password)
            session.add(user)
            session.commit()
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = session.query(User).filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Bem-vindo, {user.name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('index'))

@app.route('/criar_post', methods=['GET', 'POST'])
@login_required
def criar_post():
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('O post não pode estar vazio.', 'danger')
        else:
            post = Post(content=content, user_id=current_user.id)
            session.add(post)
            session.commit()
            flash('Post criado com sucesso!', 'success')
            return redirect(url_for('index'))
    return render_template('criar_post.html')
