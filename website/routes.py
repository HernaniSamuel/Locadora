from .models import User, Carro, Foto
from flask import render_template, Blueprint, redirect, url_for, flash
from .forms import LoginForm, RegisterForm, CarForm, AlugarForm, DevolverForm, CarEditForm, DeletarForm, EditUserForm, CarImgForm
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
                preco_base=form.preco_base.data,
                descricao=form.descricao.data,

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
    carro_alugado = Carro.query.get_or_404(carro_id)

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
    carro = Carro.query.get_or_404(carro_id)
    imagens = []
    for imagem in carro.imagem:
        imagens.append(imagem)
    imagens_json = [{'id': foto.id, 'link': foto.link} for foto in imagens]

    return render_template('car-info.html', current_user=current_user, carro=carro, imagens=imagens_json)


@routes.route('/caros_alugados', methods=['GET', 'POST'])
@login_required
def carros_alugados():
    carros_alugados = Carro.query.filter_by(locador=current_user.id)
    carros = []
    for carro in carros_alugados:
        carros.append(carro)
    return render_template('carros_alugados.html', carros=carros, current_user=current_user)


@routes.route('/devolucao/<carro_id>', methods=['GET', 'POST'])
@login_required
def devolucao(carro_id):
    carro = Carro.query.get_or_404(carro_id)
    form = DevolverForm()
    if form.validate_on_submit():
        carro.locador = None
        db.session.commit()
        flash('Devolução feita com sucesso! Iremos buscar o que é nosso.', category='success')
        return redirect(url_for('routes.home'))

    return render_template('devolucao.html', carro=carro, form=form, current_user=current_user)


@routes.route('/edicao', methods=['GET', 'POST'])
@login_required
def edicao():
    carros = Carro.query.all()
    return render_template('edicao.html', carros=carros, current_user=current_user)


@routes.route('/edicao_carro/<carro_id>', methods=['GET', 'POST'])
@login_required
def edicao_carro(carro_id):
    if current_user.role == 'manager':
        carro = Carro.query.get_or_404(carro_id)

        form = CarEditForm(obj=carro)
        if form.validate_on_submit():

            carro.nome=form.nome.data
            carro.marca=form.marca.data
            carro.ano_fabricacao=form.ano_fabricacao.data
            carro.consumo=form.consumo.data
            carro.preco_base=form.preco_base.data
            carro.descricao=form.descricao.data

            db.session.commit()

            flash(f'Veículo editado com sucesso!', category='success')

            return redirect(url_for('routes.edicao'))

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'Erro ao editar: {err_msg}', category='danger')

        return render_template('edicao_carro.html', form=form, current_user=current_user, carro=carro)

    else:
        flash('Esta página é apenas para administradores!', category='danger')
        return redirect(url_for('routes.home'))


@routes.route('/delecao_carro/<carro_id>', methods=['GET', 'POST'])
@login_required
def delecao_carro(carro_id):
    if current_user.role == 'manager':
        carro = Carro.query.get_or_404(carro_id)
        form = DeletarForm()
        if form.validate_on_submit():
            db.session.delete(carro)
            db.session.commit()
            flash('O carro foi deletado!', category='success')
            return redirect(url_for('routes.home'))

        return render_template('delecao_carro.html', carro=carro, form=form, current_user=current_user)
    else:
        flash('Esta página é apenas para administradores!', category='danger')
        return redirect(url_for('routes.home'))


@routes.route('/edicao_perfil', methods=['GET', 'POST'])
@login_required
def edicao_perfil():
    form = EditUserForm(obj=current_user, current_user=current_user)
    if form.validate_on_submit():
        current_user.nome=form.nome.data
        current_user.identidade=form.identidade.data
        current_user.carteira_motorista=form.carteira_motorista.data
        current_user.telefone=form.telefone.data
        current_user.email=form.email.data
        current_user.endereco=form.endereco.data
        current_user.senha=form.password1.data

        db.session.commit()
        flash('Perfil alterado com sucesso!', category='success')
        return redirect(url_for('routes.home'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Erro ao editar: {err_msg}', category='danger')

    return render_template('edit_profile.html', current_user=current_user, form=form)


@routes.route('/delecao_perfil', methods=['GET', 'POST'])
@login_required
def delecao_perfil():
    if current_user.role == 'client':
        form = DeletarForm()
        if form.validate_on_submit():

            carros = Carro.query.filter_by(locador=current_user.id)
            for carro in carros:
                carro.locador=None
                db.session.commit()

            db.session.delete(current_user)
            db.session.commit()
            flash('Conta deletada com sucesso! Faça outra quando quiser!', category='success')
            return redirect(url_for('routes.home'))

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'Erro ao deletar: {err_msg}', category='danger')

        return render_template('delete_user.html', current_user=current_user, form=form)
    else:
        flash('A conta de superusuário não pode ser apagada!', category='danger')
        return redirect(url_for('routes.home'))


@routes.route('/adicionar_imagem/<carro_id>', methods=['GET', 'POST'])
@login_required
def adicionar_imagem(carro_id):
    if current_user.role == 'manager':
        carro = Carro.query.get_or_404(carro_id)
        form = CarImgForm()
        if form.validate_on_submit():
            imagem = Foto(link=form.link.data, carro=carro.id)
            db.session.add(imagem)
            db.session.commit()
            return redirect(url_for('routes.adicionar_imagem', carro_id=carro_id))

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'Erro ao adicionar imagem: {err_msg}', category='danger')

        return render_template('CarImg.html', current_user=current_user, form=form)

    else:
        flash('Esta página é apenas para administradores!', category='danger')
        return redirect(url_for('routes.home'))
