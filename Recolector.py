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

            labels = onto.search(label="*"+word+"*",_case_sensitive=False)
            coincidencias.extend(labels)
            for label in labels:

    #kargs= {'k' : "has_"+word, 'v0' : "*"}
    #things.extend(onto.search(has_Artista = "*")) Nada de esto ha servido para buscar cosas relaconadas
                '''
                Podría simplemente darle coincidencias.extend(onto.search(is_a=label))
                Eso admitiría los duplicados y gastaría memoria.
                Esta forma evita los duplicados y gasta procesamiento.
                Toca hacer pruebas y ver qué es más crítico para elegir bien. 
                '''
                things = onto.search(is_a=label)
                for thing in things:
                    print(thing.label, coincidencias.count(thing))
                    if coincidencias.count(thing) == 0:
                        coincidencias.append(thing)

    return Generador.generarOnto(coincidencias)