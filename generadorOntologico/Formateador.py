from io import BytesIO
from util import util

def formatearOnto(OntoGenerada, formato):
    try:
        if(formato == "json"):
            result = toJSON_LD(OntoGenerada)
        elif (formato == "nt"):
            result = toNTriples(OntoGenerada)
        else:
            result = toRDF(OntoGenerada)
        return result
    except:
        util.printException(Exception, "formateardor.formatearOnto")
        return "Error al convertir la ontología al formato solicitado"

def toJSON_LD(OntoGenerada):

    g = OntoGenerada.world.as_rdflib_graph()
    result = g.serialize(format='json-ld', indent=4).decode('utf-8')

    return result

def toRDF(OntoGenerada):
    virtualFile = BytesIO()
    OntoGenerada.save(virtualFile)

    result = virtualFile.getvalue().decode('utf8')

    virtualFile.close()
    return result

def toNTriples(OntoGenerada):
    virtualFile = BytesIO()
    OntoGenerada.save(virtualFile, format = "ntriples")

    result = virtualFile.getvalue().decode('utf-8')

    virtualFile.close()
    return result