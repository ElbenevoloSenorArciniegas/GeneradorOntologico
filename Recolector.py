#from owlready2 import default_world

import AdminFuentes
import Generador

def buscar(keyWords):

    default_world = AdminFuentes.getWorld()

    # Método de búsqueda
    #articles = default_world.search(label=FTS(keyWords)) ¿Qué es FTS?

    coincidencias = []
    '''
    #has_toppings = [] No sé qué sea topping, pero es bueno no olvidar que existe
    # has_toppings.append(onto.search(has_topping ="*" + word + "*",_case_sensitive=False))
    '''

    for word in keyWords:
        print(word)

        for onto_key in default_world.ontologies.keys():
            print(onto_key)
            onto = default_world.get_ontology(onto_key)

            coincidencias.append(onto.search(label="*"+word+"*",_case_sensitive=False))

    return Generador.generarOnto(coincidencias)