from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.widgets import PasswordInput
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from .models import User
from datetime import datetime


class LoginForm(FlaskForm):
    nome = StringField(label='Nome', validators=[Length(min=2, max=50), DataRequired()])
    password = PasswordField(label='Senha', widget=PasswordInput(hide_value=False), validators=[DataRequired()])
    submit = SubmitField(label='Entrar')


class RegisterForm(FlaskForm):
    def validate_nome(self, nome_to_check):
        user = User.query.filter_by(nome=nome_to_check.data).first()
        if user:
            raise ValidationError("Nome de usuário já cadastrado!")

    def validate_identidade(self, identidade_to_check):
        identidade = User.query.filter_by(identidade=identidade_to_check.data).first()
        if identidade:
            raise ValidationError("Identidade já cadastrada!")

    def validate_carteira_motorista(self, carteira_motorista_to_check):
        carteira_motorista = User.query.filter_by(carteira_motorista=carteira_motorista_to_check.data).first()
        if carteira_motorista:
            raise ValidationError("CNH já cadastrada!")

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email já cadastrado!")


    nome = StringField(label='Nome', validators=[Length(min=2, max=50), DataRequired()])
    identidade = StringField(label='Identidade', validators=[Length(min=8, max=15), DataRequired()])
    carteira_motorista = StringField(label='CNH', validators=[Length(max=11), DataRequired()])
    telefone = StringField(label='Telefone', validators=[Length(max=20), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    endereco = StringField(label='Endereço', validators=[Length(max=500), DataRequired()])
    password1 = PasswordField(label='Senha', validators=[Length(min=6, max=16), DataRequired()])
    password2 = PasswordField(label='Confirmar senha', validators=[EqualTo('password1')])
    submit = SubmitField(label='Cadastrar!')


class EditUserForm(FlaskForm):
    def __init__(self, current_user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.user_id = current_user.id

    def validate_nome(self, nome_to_check):
        user = User.query.filter_by(nome=nome_to_check.data).first()
        if user and user.id != self.user_id:
            raise ValidationError("Nome de usuário já cadastrado!")

    def validate_identidade(self, identidade_to_check):
        identidade = User.query.filter_by(identidade=identidade_to_check.data).first()
        if identidade and identidade.id != self.user_id:
            raise ValidationError("Identidade já cadastrada!")

    def validate_carteira_motorista(self, carteira_motorista_to_check):
        carteira_motorista = User.query.filter_by(carteira_motorista=carteira_motorista_to_check.data).first()
        if carteira_motorista and carteira_motorista.id != self.user_id:
            raise ValidationError("CNH já cadastrada!")

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email and email.id != self.user_id:
            raise ValidationError("Email já cadastrado!")


    nome = StringField(label='Nome', validators=[Length(min=2, max=50), DataRequired()])
    identidade = StringField(label='Identidade', validators=[Length(min=8, max=15), DataRequired()])
    carteira_motorista = StringField(label='CNH', validators=[Length(max=11), DataRequired()])
    telefone = StringField(label='Telefone', validators=[Length(max=20), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    endereco = StringField(label='Endereço', validators=[Length(max=500), DataRequired()])
    password1 = PasswordField(label='Senha', validators=[Length(min=6, max=16), DataRequired()])
    password2 = PasswordField(label='Confirmar senha', validators=[EqualTo('password1')])
    submit = SubmitField(label='Editar')


class CarForm(FlaskForm):
     nome = StringField(label='Nome', validators=[Length(max=30), DataRequired()])
     marca = StringField(label='Marca', validators=[Length(max=30), DataRequired()])
     ano_fabricacao = IntegerField(label='Ano de fabricação', validators=[DataRequired(), NumberRange(min=1870, max=datetime.utcnow().year)])
     consumo = FloatField(label='Consumo (km/l)', validators=[DataRequired()])
     preco_base = FloatField(label='Preço base', validators=[DataRequired()])
     descricao = StringField(label='Descrição', validators=[Length(max=500)])


     submit = SubmitField(label='Cadastrar!')


class CarEditForm(FlaskForm):
    nome = StringField(label='Nome', validators=[Length(max=30), DataRequired()])
    marca = StringField(label='Marca', validators=[Length(max=30), DataRequired()])
    ano_fabricacao = IntegerField(label='Ano de fabricação',
                                  validators=[DataRequired(), NumberRange(min=1870, max=datetime.utcnow().year)])
    consumo = FloatField(label='Consumo (km/l)', validators=[DataRequired()])
    preco_base = FloatField(label='Preço base', validators=[DataRequired()])
    descricao = StringField(label='Descrição', validators=[Length(max=500)])

    submit = SubmitField(label='Editar')


class AlugarForm(FlaskForm):
    submit = SubmitField(label='Alugar!')


class DevolverForm(FlaskForm):
    submit = SubmitField(label='Devolver')


class DeletarForm(FlaskForm):
    submit = SubmitField(label='Deletar')


class CarImgForm(FlaskForm):
    link = StringField(label='Link da imagem', validators=[DataRequired()])
    submit = SubmitField(label='Adicionar')
