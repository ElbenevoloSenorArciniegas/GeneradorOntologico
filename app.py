import Recolector
import Formateador
import AdminFuentes

from markupsafe import escape
from flask import Flask, request, render_template
import Generador

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

    # --------------------------------------------------------------------
    #estoy mirando y probando cosas directamente, no es que esto vaya aquí
    '''
    world = Generador.tempWorld
    for triple in OntoGenerada.get_triples():
        print(triple)
        try:
            for x in triple:
                print(world._unabbreviate(x))
        except:
            print(x)
    '''
    #--------------------------------------------------------------------

    if(formato == "json"):
        result = Formateador.toJSON_LD(OntoGenerada)
    elif (formato == "nt"):
        result = Formateador.toNTriples(OntoGenerada)
    else:
        result = Formateador.toRDF(OntoGenerada)

    Generador.cleanTempWorld()
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

##Borrar: sólo para usos de pruebas rápidas
@app.route('/getStringSimilarity')
def getStringSimilarity():
    str1 = request.args.get("str1", "").lower()
    str2 = request.args.get("str2", "").lower()
    return str1 + " -> " +str2 +" : "+ str(Recolector.getStringSimilarity(str1, str2))


import werkzeug.serving
werkzeug.serving.run_simple("localhost", 5000, app)