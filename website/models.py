from . import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(length=50), unique=True, nullable=False)
    identidade = db.Column(db.String(length=15), unique=True, nullable=False)
    carteira_motorista = db.Column(db.String(length=11), unique=True, nullable=False)
    telefone = db.Column(db.String(length=20), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    endereco = db.Column(db.String(length=500), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    carros = db.relationship('Carro', backref='alugado', lazy=True)
    role = db.Column(db.String(), default='client') # 'manager' é o administrador

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Carro(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(length=30), nullable=False)
    marca = db.Column(db.String(length=30), nullable=False)
    ano_fabricacao = db.Column(db.Integer(), nullable=False)
    consumo = db.Column(db.Float(), nullable=False)
    locador = db.Column(db.Integer(), db.ForeignKey('user.id'))
    preco_base = db.Column(db.Float(), nullable=False)
