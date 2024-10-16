from flask import Flask, request, session, jsonify
from api.models import db, Car, CarType, User
from api.config import Config
from api.utils.logger import logger
from dotenv import load_dotenv
import os

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db.init_app(app)

@app.route('/login', methods=['POST'])
def login(): #metodo para fazer login e autenticação do usuário
    logger.info("Iniciando serviço de login.")

    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        password = data['password']

        user = User.query.filter_by(name=name).first()

        if user and (user.password == password): #verifica se a senha digitada está correta
            session['user_id'] = user.id
            session['name'] = user.name
            return jsonify({
                "message": "Usuário logado com sucesso.",
                "user_id": user.id,
                "user_name": user.name
                }), 200

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)

@app.route('/new_user', methods=['POST'])
def new_user():
    logger.info("Iniciando serviço de cadastro de novo usuário.")

    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        password = data['password']
        new_user = User(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "Usuário cadastrado com sucesso.",
            "user_id": new_user.id,
            "user_name": new_user.name
        }), 200

@app.route('/')
def index(): #página inicial que mostra todos os veículos cadastrados 
    # if 'user_id' not in session: #se o usuário não está logado redireciona para a página de login
    #     return redirect(url_for('login'))

    user_id = session['user_id']
    cars = Car.query.filter_by(user_id=user_id).all()
    car_types = CarType.query.all()
    return jsonify({
        "cars": cars,
        "car_types": car_types
    })

@app.route('/new', methods=['POST'])
def new_car(): #adiciona um novo veículo
    logger.info('Iniciando serviço de cadastrar novo veículo.')
    
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        year = data['year']
        description = data['description']
        type_id = data['type_id']
        user_id = session['user_id']
        new_car = Car(name=name, year=year, description=description, type_id=type_id, user_id=user_id)
        db.session.add(new_car)
        db.session.commit()
        return jsonify({
            "message": "Veículo cadastrado com sucesso.",
            "user_id": user_id,
            "car_name": name
        }), 200

@app.route('/edit/<int:id>', methods=['POST'])
def edit_car(id): #edita o veículo com o id selecionado
    logger.info('Iniciando serviço de editar veículo.')

    car = Car.query.get_or_404(id)
    if request.method == 'POST':
        data = request.get_json()
        car.name = data['name']
        car.year = data['year']
        car.description = data['description']
        car.type_id = data['type_id']
        db.session.commit()
        return jsonify({
            "message": "Veículo editado com sucesso.",
            "user_id": car.user_id,
            "car_name": car.name
        }), 200

@app.route('/delete/<int:id>')
def delete_car(id): #deleta o veículo com o id selecionado
    logger.info('Iniciando serviço de excluir veículo.')

    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({
        "message": "Veículo excluído com sucesso.",
        "user_id": car.user_id,
        "car_name": car.name
    }), 200

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
