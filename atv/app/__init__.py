from flask import Flask, render_template
from users import users
from numeros import numeros

app = Flask (__name__, template_folder='templates')

app.register_blueprint(users.bp)
app.register_blueprint(numeros.bp)

@app.route('/')
def index():
    return render_template('auth.html')