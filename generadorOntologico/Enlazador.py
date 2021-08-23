import requests
import urllib
from owlready2 import Ontology, types, Thing
from exploradorRecursos import AdminFuentes

default_world = AdminFuentes.getMoK()
OntoDbPedia = Ontology(world=default_world, base_iri="http://dbpedia.org/resource/")


def buscarURIEnlaceWordnet(etiqueta):
    url = "https://lookup.dbpedia.org/api/search/KeywordSearch?MaxHits=1&QueryString="
    params = urllib.parse.quote_plus(etiqueta)
    response = requests.get(url+"%22"+params+"%22")
    result = response.text
    uriInicio = result.find("<URI>")
    uriFin = result.find("</URI>")
    if uriInicio != -1 and uriFin != -1:
        nombreConcepto = result[uriInicio+5:uriFin]
        nombreConcepto = nombreConcepto[nombreConcepto.rindex("/")+1:]
        return enlazarConceptos(nombreConcepto)
    return None


def enlazarConceptos(nombreConceptoDbPedia):
    with OntoDbPedia:
        conceptoDbPedia = types.new_class(nombreConceptoDbPedia, (Thing,))

    return conceptoDbPedia