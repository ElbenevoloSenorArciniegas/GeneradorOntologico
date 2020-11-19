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
                    prepareAssociatedClasses(obj, onto)
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
        "properties": list(get_possible_class_properties(result, default_world)),
        "parents": [],
        "children": [],
        "labels": result.label,
        "arregloDeTerminos": [],
        "similitudesSintacticas": [],
        "promedioSimilitudes": 0,
        "similitudAKeywords": []
    }
    return obj

def prepareAssociatedClasses(obj, onto):
    for parent in onto.get_parents_of(obj["obj"]):
        o = prepareDeeperObject(parent, onto)
        obj["parents"].append(o)
    for child in onto.get_children_of(obj["obj"]):
        o = prepareDeeperObject(child)
        obj["children"].append(o)
    '''
        obj["obj"].is_a
        # obj["subClasses"]= list(get_subClasses(obj["obj"],default_world))
        Estos dos diablillos (is_a y subClasses) están saturando todo y demoran demasiado el proceso.
        Es supremamente ineficiente
    '''
    return obj

def prepareDeeperObject(result,onto):
    if not result.name == "Thing":
        obj = {
            "obj": result,
            "properties": list(get_possible_class_properties(result, default_world)),
            "parents": onto.get_parents_of(result),
            "children": onto.get_children_of(result),
            "labels": result.label
        }
    else:
        obj = {
            "obj": result,
            "properties": [],
            "parents": [],
            "children": [],
            "labels": result.label
        }
    return obj

def get_possible_class_properties(Class, world):
    try:
        for prop in world.properties():
            #print(prop, prop.domain, prop.range,Class)
            for domain in prop.domain:
                if issubclass(Class, domain): yield prop
            for range in prop.range:
                if issubclass(Class, range): yield prop
    except: pass

def get_subClasses(Class, world):
    try:
        for otherClass in world.classes():
            if issubclass(otherClass, Class): yield otherClass
    except:
        pass

