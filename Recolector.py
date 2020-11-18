import AdminFuentes
import Comparador
import Generador
from owlready2 import individual, owl_restriction, owl_class

default_world = AdminFuentes.getWorld()

def buscar(keyWords):

    coincidencias = []

    for word in keyWords:

        results = default_world.search(label="* " + word + "*", type= owl_class, _case_sensitive=False)
        results.extend(default_world.search(label="*" + word + " *", type=owl_class, _case_sensitive=False))
        '''
        results.extend(default_world.search(name="* " + word + "*", type= owl_class, _case_sensitive=False))
        results.extend(default_world.search(name="*" + word + " *", type=owl_class, _case_sensitive=False))
        '''

        for result in results:
            coincidencias.append(prepareObject(result))

        for onto_key in default_world.ontologies.keys():
            #print(onto_key)
            onto = default_world.get_ontology(onto_key)

            #print("########################################################")
            for obj in coincidencias:
                try:
                    '''
                    obj["parents"] = list(prepareObjects(onto.get_parents_of(obj["obj"])))
                    obj["children"] = list(prepareObjects(onto.get_children_of(obj["obj"])))
                    obj["is_a"] = list(prepareObjects(list(obj["obj"].is_a)))
                    '''
                    prepareAssociatedClasses(obj, onto)

                except:
                    pass
                #print(obj)
            #print(obj)
            #print("########################################################")

        #print(coincidencias)
    coincidencias = Comparador.limpiarCoincidencias(coincidencias,keyWords)

    return Generador.generarOnto(keyWords[0],coincidencias)
'''
#####################################################################################
'''
def prepareAssociatedClasses(obj, onto, goDeeper= True):
    #print(goDeeper,obj)
    for parent in onto.get_parents_of(obj["obj"]):
        o = prepareDeeperObject(parent, onto)
        '''
        if not goDeeper:
            o = prepareAssociatedClasses(o, onto, False)
        '''
        obj["parents"].append(o)
    for child in onto.get_children_of(obj["obj"]):
        o = prepareDeeperObject(child)
        '''
        if not goDeeper:
            o = prepareAssociatedClasses(o, onto, False)
        '''
        obj["children"].append(o)
    '''
        for isA in list(obj["obj"].is_a):
        if (goDeeper):
            o = prepareDeeperObject(isA)
            o = prepareAssociatedClasses(o, onto, False)
        else:
            o = prepareObject(isA)
        obj["is_a"].append(o)
         # obj["subClasses"]= list(get_subClasses(obj["obj"],default_world))
         Estos dos diablillos (is_a y subClasses) están saturando todo y demoran demasiado el proceso.
         Es supremamente ineficiente
    '''

    obj["properties"] = list(get_possible_class_properties(obj["obj"], default_world))
    obj["labels"] = obj["obj"].label
    return obj

def prepareObject(result):
    obj = {
        "obj": result,
        "properties": [],
        "parents": [],
        "children": [],
        "labels": [],
        "arregloDeTerminos": [],
        "similitudesSintacticas": [],
        "promedioSimilitudes": 0,
        "similitudAKeywords": []
    }
    return obj

def prepareDeeperObject(result,onto):
    obj = {
        "obj": result,
        "properties": list(get_possible_class_properties(result, default_world)),
        "parents": onto.get_parents_of(result),
        "children": onto.get_children_of(result),
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

