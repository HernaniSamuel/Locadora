from website.models import User, db
from website import create_app
app = create_app()


if __name__ == '__main__':
    with app.app_context():
        new_manager = User(
            nome='Administrador',
            identidade='123.456.789-00',
            carteira_motorista='09876543211',
            telefone='(55)55555-5555',
            email='administrador@gmail.com',
            endereco='rua adm numero 1',
            password_hash='$2b$12$mLp.u56G72d9RCguT39xc.dHDiFYictLlEhficyEyKozpfuAlXDl2', # administrador
            role='manager'
        )
        db.session.add(new_manager)
        db.session.commit()
        print(new_manager, ' adicionado com sucesso!')
