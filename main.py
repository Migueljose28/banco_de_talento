from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required
from models import User
from db import db


app = Flask(__name__)
app.secret_key = 'admin'
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)


@lm.user_loader
def load_user(id):
    usuario = db.session.query(User).filter_by(id=id).first()
    return usuario


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']


        usuario_login = db.session.query(User).filter_by(nome=nome, senha=senha).first()

        if not usuario_login:
             return render_template('login.html', mensagem='Usuário ou senha inválidos')
    
        login_user(usuario_login)
        
        return redirect(url_for('index'))
        
        
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']

        user = User(nome=nome, senha=senha)
        db.session.add(user)
        db.session.commit()
  
        login_user(user)

        return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        
    app.run(debug=True)
