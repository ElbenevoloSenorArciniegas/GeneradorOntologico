import time

from owlready2 import close_world, Ontology, types, sync_reasoner, set_log_level, Thing, World
from exploradorRecursos import AdminFuentes
from generadorOntologico import Enlazador
from util import util

#set_log_level(9)

default_world = AdminFuentes.getBDO()
OntoGenerada = None

mutex = 0


def generarOnto(mainSubject, keyWords, coincidencias):
    '''
    :param mainSubject: El tema que se usará como id de la ontología
    :param coincidencias: Arreglo de objetos seleccionados en la búsqueda, que poblarán la ontología.
    :return: OntoGenerada:  Ontología generada y poblada a la que se le aplica el razonador.
    '''

    #print(len(coincidencias))
    #print(mainSubject)

    global OntoGenerada
    global mutex
    OntoGenerada = Ontology(world=default_world, base_iri=mainSubject + "#")

    with OntoGenerada:
        claseRaiz = types.new_class(mainSubject, (Thing,))
        claseRaiz.label = mainSubject
        mutex -= 1
        Enlazador.enlazarConDbPedia(mainSubject, claseRaiz)

        for keyword in keyWords:
            word = keyword["keyword"]
            clasePrincipal = types.new_class(word, (claseRaiz,))
            clasePrincipal.label = word
            keyword["clase"] = clasePrincipal
            mutex -= 1
            Enlazador.enlazarConDbPedia(word, clasePrincipal)

    poblarOnto(coincidencias, keyWords)

    print("\n\nEsperando por peticiones")
    while mutex < 0:
        time.sleep(0.1)
        pass
    print("Peticiones finalizadas")

    util.imprimirOntoGenerada(OntoGenerada)

    close_world(default_world)
    return razonar()
    # return  OntoGenerada


def poblarOnto(coincidencias, keyWords):
    global mutex
    global OntoGenerada
    with OntoGenerada:
        for coincidencia in coincidencias:

            claseOrigen = coincidencia["obj"]
            claseDestino = types.new_class(claseOrigen.name, (Thing,))
            claseDestino.label = claseOrigen.label
            claseDestino.equivalent_to.append(claseOrigen)

            for equivalente in coincidencia["equivalentes"]:
                claseDestino.equivalent_to.append(equivalente)

            for superclase in coincidencia["superclases"]:
                claseDestino.is_a.append(superclase)

            mutex -= 1

            Enlazador.OntoGenerada = OntoGenerada
            Enlazador.enlazarConDbPedia(coincidencia["label"], claseDestino)
            Enlazador.enlazarConConceptosLocales(claseDestino, coincidencia, keyWords)


def continuarProceso():
    global mutex
    mutex += 1
    #print(mutex)


def razonar():
    global OntoGenerada
    try:
        with OntoGenerada:
            sync_reasoner()
    except Exception:
        util.printException(Exception, "Generador.razonar")
    return OntoGenerada


def closeOnto(mainSubject):
    from exploradorRecursos import AdminFuentes

    default_world = AdminFuentes.getBDO()
    default_world.get_ontology(mainSubject + "#").destroy()
    default_world.get_ontology("http://dbpedia.org/resource/").destroy()
    default_world.save()
#    tempWorld.ontologies.clear()
#    tempWorld.close()
