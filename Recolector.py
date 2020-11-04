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

            print("########################################################")
            for label in labels:
                print(str(label))
            print("########################################################")
            coincidencias.extend(labels)
            for label in labels:
                '''
                Podría simplemente darle coincidencias.extend(onto.search(is_a=label))
                Eso admitiría los duplicados y gastaría memoria.
                Esta forma evita los duplicados y gasta procesamiento.
                Toca hacer pruebas y ver qué es más crítico para elegir bien. 
                
                ¿Esto es necesario: OntoGenerada.get_children_of()? Para escoger las cosas como si fueran
                sub-árboles donde cada raiz sea una coincidencia de keyword...
                '''
                things = onto.search(is_a=label)
                #things.extend(onto.search(**{"*"+word+"*" : "*"},_case_sensitive=False)) no ha sido útil.
                for thing in things:
                    print(thing.label, coincidencias.count(thing))
                    if coincidencias.count(thing) == 0:
                        coincidencias.append(thing)

    return Generador.generarOnto(keyWords[0],coincidencias)