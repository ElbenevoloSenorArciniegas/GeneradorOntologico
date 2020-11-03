import Recolector
import Formateador
import AdminFuentes

from markupsafe import escape
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

#Requiere Flask 1.1 para lo de los parámetros dentro de la ruta

@app.route('/search')
def buscar():
    keyWords = request.args.get("keyWords", "").split("-")
    formato = request.args.get("format", "").lower()

    OntoGenerada = Recolector.buscar(keyWords)

    if(formato == "json"):
        result = Formateador.toJSON_LD(OntoGenerada)
    elif (formato == "nt"):
        result = Formateador.toNTriples(OntoGenerada)
    else:
        result = Formateador.toRDF(OntoGenerada)

    return "Buscar( "+ request.args.get("keyWords", "") +" ) <hr> " + result


@app.route('/add/<path:IRI>')
def addFuenteExterna(IRI):
    return AdminFuentes.addFuenteExterna(IRI)

@app.route('/add/local/<path:file_name>')
def addFuenteLocal(file_name):
    return AdminFuentes.addFuenteLocal(file_name)

@app.route('/remove/<path:IRI>')
def removeFuente(IRI):
    return AdminFuentes.removeFuente(IRI)

@app.route('/getFuentes')
def getFuentes():
    return AdminFuentes.listarKeysWorld()


import werkzeug.serving
werkzeug.serving.run_simple("localhost", 5000, app)