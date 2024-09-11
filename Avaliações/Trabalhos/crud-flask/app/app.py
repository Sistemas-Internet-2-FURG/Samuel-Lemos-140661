from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Car, CarType, User
from config import Config
from utils.logger import logger
from dotenv import load_dotenv
import os

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login(): #metodo para fazer login e autenticação do usuário
    logger.info("Iniciando serviço de login.")

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()

        if user and (user.password == password): #verifica se a senha digitada está correta
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    return redirect(url_for('login'))

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    logger.info("Iniciando serviço de cadastro de novo usuário.")

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        new_user = User(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('new_user.html')

@app.route('/')
def index(): #página inicial que mostra todos os veículos cadastrados 
    if 'user_id' not in session: #se o usuário não está logado redireciona para a página de login
        return redirect(url_for('login'))

    user_id = session['user_id']
    cars = Car.query.filter_by(user_id=user_id).all()
    car_types = CarType.query.all()
    return render_template('index.html', cars=cars, car_types=car_types)

@app.route('/new', methods=['GET', 'POST'])
def new_car(): #adiciona um novo veículo
    logger.info('Iniciando serviço de cadastrar novo veículo.')
    
    car_types = CarType.query.all()
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        description = request.form['description']
        type_id = request.form['type_id']
        user_id = session['user_id']
        new_car = Car(name=name, year=year, description=description, type_id=type_id, user_id=user_id)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('new_car.html', car_types=car_types)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_car(id): #edita o veículo com o id selecionado
    logger.info('Iniciando serviço de editar veículo.')
    
    if car.user_id != session.get('user_id'): #verificar se o veículo pertence ao usuário logado
        logger.warning(f"Usuário {session.get('user_id')} tentou editar um veículo que não é dele.")
        return redirect(url_for('index'))

    car = Car.query.get_or_404(id)
    car_types = CarType.query.all()
    if request.method == 'POST':
        car.name = request.form['name']
        car.year = request.form['year']
        car.description = request.form['description']
        car.type_id = request.form['type_id']
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_car.html', car=car, car_types=car_types)

@app.route('/delete/<int:id>')
def delete_car(id): #deleta o veículo com o id selecionado
    logger.info('Iniciando serviço de excluir veículo.')
    
    if car.user_id != session.get('user_id'): #verificar se o veículo pertence ao usuário logado
        logger.warning(f"Usuário {session.get('user_id')} tentou excluir um veículo que não é dele.")
        return redirect(url_for('index'))

    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('index'))

load_dotenv()
if __name__ == '__main__':
    print('Server is running.')
    logger.info("Server is running.")
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(
        port=os.getenv("PORT"),
        host=os.getenv("HOST"),
        debug=os.getenv("DEBUG")
        )
