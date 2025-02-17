from flask import Flask, request, jsonify
from api.models import db, Car, User
from api.config import Config
from api.utils.logger import logger
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login(): #metodo para fazer login e autenticação do usuário
    logger.info("Iniciando serviço de login.")

    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    user = User.query.filter_by(name=name).first()

    if not user or user.password != password:
        return jsonify({"message": "Credenciais inválidas!"}), 401

    token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Usuário logado com sucesso.",
        "token": token
        }), 200

@app.route('/register', methods=['POST'])
def register():
    logger.info("Iniciando serviço de cadastro de novo usuário.")

    data = request.get_json()
    name = data.get("name")
    password = data.get("password")
    
    if User.query.filter_by(name=name).first():
        return jsonify({"message": "Usuário já existe!"}), 400
    
    new_user = User(name=name, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Usuário cadastrado com sucesso.",
        "user_id": new_user.id,
        "user_name": new_user.name
    }), 201

@app.route('/')
@jwt_required()
def index(): #página inicial que mostra todos os veículos cadastrados 
    user_id = get_jwt_identity()
    cars = Car.query.filter_by(user_id=user_id).all()

    cars_response = []
    for car in cars:
        car_dict = {
            "id": car.id,
            "name": car.name,
            "year": car.year,
            "description": car.description,
            # "type_id": car.type_id,
            # "type_name": car.car_type.name,
            "user_id": car.user_id
        }
        cars_response.append(car_dict)

    return jsonify({
        "cars": cars_response
    }), 200

'''@app.route('/getTypes', methods=['GET'])
@jwt_required()
def get_types():
    logger.info('Iniciando serviço de buscar tipos de carros.')

    car_types = CarType.query.all()

    car_types_response = []
    for car_type in car_types:
        car_types_response.append({
            "id": car_type.id,
            "name": car_type.name
        })

    return jsonify({
        "car_types": car_types_response
    }), 200'''

@app.route('/getCarById/<int:id>', methods=['GET'])
@jwt_required()
def get_car_by_id(id):
    logger.info('Iniciando serviço de buscar carro pelo id.')

    car = Car.query.get_or_404(id)
    if not car:
        return jsonify({"message": "Veículo não encontrado."}), 404

    car_dict = {
            "id": car.id,
            "name": car.name,
            "year": car.year,
            "description": car.description,
            # "type_id": car.type_id,
            # "type_name": car.car_type.name,
            "user_id": car.user_id
        }
    
    return car_dict, 200
    
@app.route('/new', methods=['POST'])
@jwt_required()
def new_car(): #adiciona um novo veículo
    logger.info('Iniciando serviço de cadastrar novo veículo.')
    
    user_id = get_jwt_identity()
    
    data = request.get_json()
    name = data.get("name")
    year = data.get("year")
    description = data.get("description")
    # type_id = data.get("type_id")

    new_car = Car(name=name, year=year, description=description, user_id=user_id)
    db.session.add(new_car)
    db.session.commit()

    return jsonify({
        "message": "Veículo cadastrado com sucesso.",
        "user_id": user_id,
        "car_name": name
    }), 201

@app.route('/edit/<int:id>', methods=['POST'])
@jwt_required()
def edit_car(id): #edita o veículo com o id selecionado
    logger.info('Iniciando serviço de editar veículo.')

    user_id = get_jwt_identity()
    car = Car.query.get_or_404(id)

    if car.user_id != user_id:
        return jsonify({"message": "Veículo não pertence a este usuário!"}), 401
    
    data = request.get_json()
    car.name = data.get("name")
    car.year = data.get("year")
    car.description = data.get("description")
    #car.type_id = data.get("type_id")
    db.session.commit()

    return jsonify({
        "message": "Veículo editado com sucesso.",
        "user_id": car.user_id,
        "car_name": car.name
    }), 200

@app.route('/delete/<int:id>')
@jwt_required()
def delete_car(id): #deleta o veículo com o id selecionado
    logger.info('Iniciando serviço de excluir veículo.')

    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()

    return jsonify({
        "message": "Veículo deletado com sucesso.",
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
