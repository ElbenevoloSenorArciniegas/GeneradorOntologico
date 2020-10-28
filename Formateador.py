from rdflib import Graph
from io import *

def formatear(OntoGenerada):
    # Usar la JSON-LD library

    RDF = BytesIO()
    OntoGenerada.save(RDF)

    g = Graph().parse(data=RDF.getvalue().decode('utf-8'), format='application/rdf+xml')
    result = g.serialize(format='json-ld', indent=4).decode('utf-8')

    return str(result)