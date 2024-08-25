from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def pagina_inicial():
    return render_template('index.html')

@app.route("/home", methods=['GET', 'POST'])
def cad_aluno():
    return render_template('home.html')
    
if __name__ == "__main__":
    app.run(debug=True)
    