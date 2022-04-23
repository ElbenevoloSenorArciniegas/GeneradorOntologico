from generadorOntologico import Comparador, Generador, Formateador, PreProcesador
from exploradorRecursos import AdminFuentes
from owlready2 import owl_class

def buscar(keyWords, umbral, formato, lang):

    global default_world
    default_world = AdminFuentes.getBDO()

    PreProcesador.setLanguage(lang)

    global keyWordsOriginales
    keyWordsOriginales = keyWords
    for i in range(len(keyWords)):
        keyword = keyWords[i]
        keyWords[i] = {
            "keyword": keyword,
            "sinonimos": [keyword]
        }

    coincidencias = busquedaExtendida(keyWords)

    nombre = ""
    for word in keyWords:
        word = word["keyword"].lower()
        nombre += word+"_"

    coincidencias = Comparador.limpiarCoincidencias(coincidencias,keyWords, umbral)

    ontoGenerada = Generador.generarOnto(nombre[:-1],keyWords, coincidencias)

    ontoFormateada = Formateador.formatearOnto(ontoGenerada, formato)
    #AdminFuentes.closeBDO()
    Generador.closeOnto(nombre[:-1])
    return ontoFormateada
'''
#####################################################################################
'''
def busquedaExtendida(keyWords):
    coincidencias = []
    results = []

    keyWords = PreProcesador.obtenerSinonimos(keyWords)
    for keyword in keyWords:
        for word in keyword["sinonimos"]:

            arr = default_world.search(label="*" + word + "*", type= owl_class, _case_sensitive=False)
            for result in arr:
                if not result in results:
                    results.append(result)
                    #print(result.label)
                    coincidencias.append(prepareObject(result))

    for obj in coincidencias:
        try:
            recolectarTerminos(obj)
        except:
            pass

        #print(coincidencias)
    return coincidencias
'''
#####################################################################################
'''

def prepareObject(result):
    obj = {
        "obj": result,
        "label": (result.label)[0],
        "labels": result.label,
        "arregloDeTerminos": [],
        "equivalentes": [],
        "superclases": [],
        "similitudesSintacticas": [],
        "promedioDistancias": 0,
        "similitudAKeywords": 0,
        "similitudASeleccionados": 0,
        "similitud": {}
    }

    return obj

def recolectarTerminos(obj):
    if obj["arregloDeTerminos"] == []:
        obj["equivalentes"] += obj["obj"].equivalent_to
        obj["superclases"] += obj["obj"].is_a

        associatedClasses = []
        associatedClasses.extend(obj["equivalentes"])
        associatedClasses.extend(obj["superclases"])

        associatedClasses.append(obj["obj"])

        labels = []

        for property in getProperties(associatedClasses):
            if not property.label:
                if not property.name.lower() in obj["arregloDeTerminos"]:
                    obj["arregloDeTerminos"].append(property.name.lower())
            else:
                for label in property.label:
                    if not label.lower() in labels:
                        labels.append(label.lower())
        
        for asociated in associatedClasses:
            for label in asociated.label:
                if label.lower() not in labels:
                    labels.append(label.lower())


        for token in PreProcesador.limpiarLabels(labels):
            if not token in obj["arregloDeTerminos"]:
                obj["arregloDeTerminos"].append(token)
        #print(obj["label"]," : ",obj["arregloDeTerminos"])

def getProperties(objetos):
    rtn = []
    for prop in default_world.properties():
        #print(prop, prop.domain, prop.range,Class "obj" )
        for obj in objetos:
            try:
                for domain in prop.domain:
                    if issubclass(obj, domain) and prop not in rtn:
                        rtn.append(prop)
                for range in prop.range:
                    if issubclass(obj, range) and prop not in rtn:
                        rtn.append(prop)
            except: pass
    return rtn

def get_subClasses(Class, world):
    try:
        for otherClass in world.classes():
            if issubclass(otherClass, Class): yield otherClass
    except:
        pass
