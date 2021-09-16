import urllib
from generadorOntologico import Generador
from util import AsyncHttp

def buscarURIEnlaceWordnet(etiqueta, concepto):
    url = "https://lookup.dbpedia.org/api/search/KeywordSearch?MaxHits=1&QueryString="
    params = urllib.parse.quote_plus(etiqueta.replace("_", " "))
    url = url+"%22"+params+"%22"
    AsyncHttp.get_async(url,callback=procesarRespuesta, data=concepto)

def procesarRespuesta(response, concepto):
    if(response is not None):
        if(response.status_code == 200):
            result = response.text
            uriInicio = result.find("<URI>")
            uriFin = result.find("</URI>")
            if uriInicio != -1 and uriFin != -1:
                nombreConcepto = result[uriInicio + 5:uriFin]
                nombreConcepto = nombreConcepto[nombreConcepto.rindex("/") + 1:]
                Generador.enlazarConceptos(nombreConcepto, concepto)
    Generador.continuarProceso()