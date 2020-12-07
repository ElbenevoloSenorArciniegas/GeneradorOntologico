from generadorOntologico import Comparador, Generador, Formateador, PreProcesador
from exploradorRecursos import AdminFuentes
from owlready2 import owl_class

def buscar(keyWords, umbral, formato, lang):

    global default_world
    default_world = AdminFuentes.getMoK()

    PreProcesador.setLanguage(lang)
    coincidencias = busquedaExtendida(keyWords)

    nombre = ""
    for word in keyWords:
        word = word.lower()
        nombre += word+"-"
    for word in sinonimos:
        word = word.lower()

    coincidencias = Comparador.limpiarCoincidencias(coincidencias,keyWords, sinonimos, umbral)

    ontoGenerada = Generador.generarOnto(nombre[:-1],coincidencias)

    ontoFormateada = Formateador.formatearOnto(ontoGenerada, formato)
    AdminFuentes.closeMoK()
    Generador.closeMoK()
    return ontoFormateada
'''
#####################################################################################
'''
def busquedaExtendida(keyWords):
    coincidencias = []
    results = []

    global sinonimos
    sinonimos = PreProcesador.obtenerSinonimos(keyWords)
    for word in keyWords+sinonimos:

        arr = default_world.search(label="*" + word + "*", type= owl_class, _case_sensitive=False)
        for result in arr:
            if not result in results:
                results.append(result)
                #print(result.label)
                coincidencias.append(prepareObject(result))

    for onto_key in default_world.ontologies.keys():
        #print(onto_key)
        onto = default_world.get_ontology(onto_key)

        for obj in coincidencias:
            try:
                #if hasObj(onto, obj):
                recolectarTerminos(obj, onto)
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
        "labels": result.label,
        "arregloDeTerminos": [],
        "similitudesSintacticas": [],
        "promedioDistancias": 0,
        "similitudAKeywords": []
    }
    return obj

def recolectarTerminos(obj, onto):
    if obj["arregloDeTerminos"] == []:
        
        associatedClasses = []
        associatedClasses.extend(onto.get_parents_of(obj["obj"]))
        associatedClasses.extend(onto.get_children_of(obj["obj"]))
        
        deeperClasses = []
        for asociated in associatedClasses:
            if not asociated.name == "Thing":
                for deeper in onto.get_parents_of(asociated) + onto.get_children_of(asociated):
                    if not deeper in associatedClasses and not deeper in deeperClasses:
                        deeperClasses.append(deeper)
        associatedClasses.extend(deeperClasses)
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
        print(obj["labels"][0]," : ",obj["arregloDeTerminos"])

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
