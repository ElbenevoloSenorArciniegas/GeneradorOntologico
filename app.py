from generadorOntologico import Recolector
from exploradorRecursos import AdminFuentes

from flask import Flask, request, render_template
from flask_fontawesome import FontAwesome

app = Flask(__name__)
fa = FontAwesome(app)

@app.route('/')
def hello_world():
    return render_template("index.html")
"""
@app.route('/admin')
def hello_world():
    return render_template("admin.html")
"""
#Requiere Flask 1.1 para lo de los parámetros dentro de la ruta

@app.route('/search')
def buscar():
    keyWords = request.args.get("keyWords", "").split(",")
    formato = request.args.get("format", "").lower()
    print(formato)
    lang = request.args.get("lang", "").lower()
    if lang == "": lang = "eng"
    umbral = int(request.args.get("umbral", default=-1, type=int))
    print(umbral)
    if umbral == -1: umbral = 70

    OntoGenerada = Recolector.buscar(keyWords, umbral, formato, lang)

    return OntoGenerada


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