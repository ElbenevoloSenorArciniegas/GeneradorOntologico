import AdminFuentes
import Comparador
import Generador
from owlready2 import individual


def buscar(keyWords):

    default_world = AdminFuentes.getWorld()

    coincidencias = []

    for word in keyWords:

        labels = default_world.search(label="*" + word + "*", _case_sensitive=False)
        for label in labels:
            if not isinstance(label, individual.Thing):
                obj = {
                    "obj": label,
                    "properties": [],
                    "parents": [],
                    "children": [],
                    "similitudesSintacticas": []
                }
                coincidencias.append(obj)
            
        for onto_key in default_world.ontologies.keys():
            print(onto_key)
            onto = default_world.get_ontology(onto_key)

            print("########################################################")
            for obj in coincidencias:
                print(obj)
                try:
                    obj["properties"] = list(get_possible_class_properties(obj["obj"], default_world))
                    obj["parents"] = onto.get_parents_of(obj["obj"])
                    obj["children"] = onto.get_children_of(obj["obj"])
                except:
                    pass
            print("########################################################")

        print(coincidencias)
    coincidencias = Comparador.limpiarCoincidencias(coincidencias,keyWords)

    return Generador.generarOnto(keyWords[0],coincidencias)


def get_possible_class_properties(Class, world):
    try:
        for prop in world.properties():
            #print(prop, prop.domain, prop.range,Class)
            for domain in prop.domain:
                if issubclass(Class, domain): yield prop
            for range in prop.range:
                if issubclass(Class, range): yield prop
    except: pass
        #print("Esta chingadera yo no la quiero", str(Class))

#print(list(get_possible_class_properties(onto.t1)))