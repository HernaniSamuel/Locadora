from .models import User, Carro
from flask import render_template, Blueprint, redirect, url_for, flash
from .forms import LoginForm, RegisterForm, CarForm, AlugarForm
from . import db
from flask_login import login_user, current_user, logout_user, login_required

routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template('home.html', current_user=current_user)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(nome=form.nome.data).first()
        if attempted_user and attempted_user.check_password_correction(
          attempted_password = form.password.data
        ):
            login_user(attempted_user)
            flash(f'Bem-vindo(a), {attempted_user.nome}!', category='success')
            return redirect(url_for('routes.home'))
        else:
            flash('Nome ou senha errados!', category='danger')

    return render_template('login.html', form=form, current_user=current_user)


@routes.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Desconectado com sucesso, volte sempre!', category='success')
    return redirect(url_for('routes.home'))


@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            nome=form.nome.data,
            identidade=form.identidade.data,
            carteira_motorista=form.carteira_motorista.data,
            telefone=form.telefone.data,
            email=form.email.data,
            password=form.password1.data,
            endereco=form.endereco.data,
        )
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f"Cadastrado com sucesso! Bem-vindo(a), {user_to_create.nome}!", category='success')
        return redirect(url_for('routes.home'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Erro ao cadastrar: {err_msg}', category='danger')

    return render_template('register.html', form=form, current_user=current_user)


@routes.route('/car-register', methods=['GET', 'POST'])
@login_required
def car_register():
    if current_user.role == 'manager':
        form = CarForm()
        if form.validate_on_submit():
            car_to_add = Carro(
                nome=form.nome.data,
                marca=form.marca.data,
                ano_fabricacao=form.ano_fabricacao.data,
                consumo=form.consumo.data,
                preco_base=form.preco_base.data
            )
            db.session.add(car_to_add)
            db.session.commit()

            flash(f'Veículo cadastrado com sucesso!', category='success')
            return redirect(url_for('routes.car_register'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'Erro ao cadastrar: {err_msg}', category='danger')

        return render_template('car-register.html', form=form, current_user=current_user)

    else:
        flash('Esta página é apenas para administradores!', category='danger')
        return redirect(url_for('routes.home'))


@routes.route('/catalogo', methods=['GET', 'POST'])
def catalogo():
    carros = Carro.query.filter_by(locador=None)
    return render_template('catalogo.html', carros=carros, current_user=current_user)


@routes.route('/processamento/<carro_id>', methods=['GET', 'POST'])
@login_required
def processamento(carro_id):
    carro_alugado = Carro.query.filter_by(id=carro_id).first()

    form = AlugarForm()
    if form.validate_on_submit():
        carro_alugado.locador = current_user.id
        db.session.commit()
        flash(f'Alugado com sucesso! {carro_alugado.nome} está te aguardando na concessionária!', category='success')
        return redirect(url_for('routes.home'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Erro ao concluir aluguel: { err_msg }', category='danger')

    return render_template('processamento.html', carro=carro_alugado, current_user=current_user, form=form)


@routes.route('/car-info/<carro_id>', methods=['GET', 'POST'])
def car_info(carro_id):
    carro = Carro.query.filter_by(id=carro_id).first()
    return render_template('car-info.html', current_user=current_user, carro=carro)
