from rdflib import Graph
from io import *

def toJSON_LD(OntoGenerada):
    RDF = BytesIO()
    OntoGenerada.save(RDF)

    g = Graph().parse(data=RDF.getvalue().decode('utf-8'), format='application/rdf+xml')
    result = str(g.serialize(format='json-ld', indent=4).decode('utf-8'))

    RDF.close()
    return result

def toRDF(OntoGenerada):
    RDF = BytesIO()
    OntoGenerada.save(RDF)

    result = str(RDF.getvalue().decode('utf-8'))

    RDF.close()
    return result

def toNTriples(OntoGenerada):
    NT = BytesIO()
    OntoGenerada.save(NT, format = "ntriples")

    result = str(NT.getvalue().decode('utf-8'))

    NT.close()
    return result