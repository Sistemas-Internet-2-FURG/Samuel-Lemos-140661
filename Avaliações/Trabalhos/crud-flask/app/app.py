from flask import Flask, render_template, request, redirect, url_for
from models import db, Car, CarType
from config import Config
from utils.logger import logger

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index(): #página inicial que mostra todos os veículos cadastrados
    cars = Car.query.all()
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
        new_car = Car(name=name, year=year, description=description, type_id=type_id)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('new_car.html', car_types=car_types)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_car(id): #edita o veículo com o id selecionado
    logger.info('Iniciando serviço de editar veículo.')
    
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
    
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print('Server is running.')
    logger.info("Server is running.")
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(
        port=5000,
        host='127.0.0.1',
        debug=True
        )