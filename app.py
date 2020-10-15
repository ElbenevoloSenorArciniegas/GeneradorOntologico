import Recolector
import Formateador
import AdminFuentes

from markupsafe import escape

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Debo hacer una página de inicio para el proyecto, tal vez. Le daría personalidad'

#Requiere Flask 1.1 para lo de los parámetros dentro de la ruta

@app.route('/search/<keyWord>')
def buscar(keyWord):
    OntoGenerada = Recolector.buscar(keyWord)
    return "Buscar( " + keyWord + ") -> " + Formateador.formatear(OntoGenerada)


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