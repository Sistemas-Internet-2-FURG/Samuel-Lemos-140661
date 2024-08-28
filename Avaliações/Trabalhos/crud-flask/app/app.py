from flask import Flask, request, render_template
from config.db import db
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config())
db.init_app(app)

@app.route("/", methods=['GET', 'POST'])
def pagina_inicial():
    return render_template('index.html')

@app.route("/home", methods=['GET', 'POST'])
def cad_aluno():
    return render_template('home.html')
    
if __name__ == "__main__":
    app.run(
        port=5000,
        host='127.0.0.1',
        debug=True
        )
    