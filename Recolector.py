import AdminFuentes
import Comparador
import Generador
from owlready2 import individual, owl_restriction, owl_class


def buscar(keyWords):

    default_world = AdminFuentes.getWorld()

    coincidencias = []

    for word in keyWords:

        results = default_world.search(label="*" + word + "*", type= owl_class, _case_sensitive=False)
        results.extend(default_world.search(name="*" + word + "*", type= owl_class, _case_sensitive=False))
        #results.extend(default_world.search(class iri="*" + word + "*", type=owl_class, _case_sensitive=False))

        for result in results:
            #if isinstance(label, individual.Thing) :
            obj = {
                "obj": result,
                "properties": [],
                "parents": [],
                "children": [],
                "labels": [],
                "similitudesSintacticas": []
            }
            coincidencias.append(obj)

        for onto_key in default_world.ontologies.keys():
            print(onto_key)
            onto = default_world.get_ontology(onto_key)

            print("########################################################")
            for obj in coincidencias:
                try:
                    obj["properties"] = list(get_possible_class_properties(obj["obj"], default_world))
                    obj["parents"] = onto.get_parents_of(obj["obj"])
                    obj["children"] = onto.get_children_of(obj["obj"])
                    obj["labels"] = obj["obj"].label
                except:
                    pass
                print(obj)
            print("########################################################")

        #print(coincidencias)
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