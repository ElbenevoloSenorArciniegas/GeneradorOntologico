from rdflib import Graph
from io import *

def formatearOnto(OntoGenerada, formato):
    if(formato == "json"):
        result = Formateador.toJSON_LD(OntoGenerada)
    elif (formato == "nt"):
        result = Formateador.toNTriples(OntoGenerada)
    else:
        result = Formateador.toRDF(OntoGenerada)
    return result

def toJSON_LD(OntoGenerada):
    RDF = BytesIO()
    OntoGenerada.save(RDF)

    #g = Graph().parse(data=RDF.getvalue().decode('utf-8'), format='application/rdf+xml')
    g = OntoGenerada.world.as_rdflib_graph()
    result = g.serialize(format='json-ld', indent=4).decode('utf-8')

    RDF.close()
    return result

def toRDF(OntoGenerada):
    RDF = BytesIO()
    OntoGenerada.save(RDF)

    result = RDF.getvalue().decode('utf8')

    RDF.close()
    return result

def toNTriples(OntoGenerada):
    NT = BytesIO()
    OntoGenerada.save(NT, format = "ntriples")

    result = NT.getvalue().decode('utf-8')

    NT.close()
    return result