import AdminFuentes
import Comparador
import Generador
from owlready2 import owl_class

default_world = AdminFuentes.getWorld()

def buscar(keyWords):

    coincidencias = []

    for word in keyWords:

        results = default_world.search(label="* " + word + "*", type= owl_class, _case_sensitive=False)
        for result in default_world.search(label="*" + word + " *", type=owl_class, _case_sensitive=False):
            if not result in results:
                results.append(result)
        '''
        results.extend(default_world.search(name="* " + word + "*", type= owl_class, _case_sensitive=False))
        results.extend(default_world.search(name="*" + word + " *", type=owl_class, _case_sensitive=False))
        '''
        for result in results:
            coincidencias.append(prepareObject(result))

    for onto_key in default_world.ontologies.keys():
        #print(onto_key)
        onto = default_world.get_ontology(onto_key)

        for obj in coincidencias:
            try:
                tryFillObject(obj, onto)
            except:
                pass
        #print(coincidencias)

    coincidencias = Comparador.limpiarCoincidencias(coincidencias,keyWords)
    return Generador.generarOnto(keyWords[0],coincidencias)
'''
#####################################################################################
'''
def prepareObject(result):
    obj = {
        "obj": result,
        "properties": [],
        "parents": [],
        "children": [],
        "labels": result.label,
        "arregloDeTerminos": [],
        "similitudesSintacticas": [],
        "promedioSimilitudes": 0,
        "similitudAKeywords": []
    }

    return obj

def tryFillObject(obj, onto):
    associatedClasses = []
    obj["parents"] = onto.get_parents_of(obj["obj"])
    obj["children"] = onto.get_children_of(obj["obj"])
    associatedClasses.extend(obj["parents"])
    associatedClasses.extend(obj["children"])
    deeperClasses = []
    for asociated in associatedClasses:
        if not asociated.name == "Thing":
            for deeper in onto.get_parents_of(asociated) + onto.get_children_of(asociated):
                if not deeper in associatedClasses and not deeper in deeperClasses:
                    deeperClasses.append(deeper)
    associatedClasses.extend(deeperClasses)
    for property in getPropertiesNames(associatedClasses):
        if not property in obj["arregloDeTerminos"]:
            obj["arregloDeTerminos"].append(property)
    for label in obj["obj"].label:
        if label not in obj["arregloDeTerminos"]:
            obj["arregloDeTerminos"].append(label)
    for asociated in associatedClasses:
        for label in asociated.label:
            if label not in obj["arregloDeTerminos"]:
                obj["arregloDeTerminos"].append(label)

def getPropertiesNames(objetos):
    rtn = []
    for prop in default_world.properties():
        #print(prop, prop.domain, prop.range,Class "obj" )
        for obj in objetos:
            try:
                for domain in prop.domain:
                    if issubclass(obj, domain) and prop.name not in rtn: rtn.append(prop.name)
                for range in prop.range:
                    if issubclass(obj, range) and prop.name not in rtn: rtn.append(prop.name)
            except: pass
    return rtn

def get_subClasses(Class, world):
    try:
        for otherClass in world.classes():
            if issubclass(otherClass, Class): yield otherClass
    except:
        pass

'''
######################################################################################3
'''
def compararConOtrosTerminosBusqueda(obj, keywords):
    arr = obj["arregloDeTerminos"]
    mayor = 1
    for x in arr:
        x = x.lower()
        count = 0
        for word in keywords:
            word = word.lower()
            if x.find(word) > -1:
                count = count + 1
        #if(count == 0): count = 1 #Es un valor divisor en la fórmula siguiente. Es peligroso dejarlo en 0
        #obj["similitudAKeywords"].append(count)
        if count > mayor : mayor = count
    obj["similitudAKeywords"] = mayor
    #print(obj["obj"].name,obj["similitudAKeywords"])

    return obj