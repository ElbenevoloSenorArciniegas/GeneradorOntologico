import time

from owlready2 import close_world, Ontology, types, sync_reasoner, set_log_level, Thing, World, Restriction
from exploradorRecursos import AdminFuentes
from generadorOntologico import Enlazador
from util import util

#set_log_level(9)

tempWorld = World()
default_world = AdminFuentes.getMoK()

OntoDbPedia = Ontology(world=default_world, base_iri="http://dbpedia.org/resource/")
OntoGenerada = None

mutex = 0


def generarOnto(mainSubject, keyWords, coincidencias):
    '''
    :param mainSubject: El tema que se usará como id de la ontología
    :param coincidencias: Arreglo de objetos seleccionados en la búsqueda, que poblarán la ontología.
    :return: OntoGenerada:  Ontología generada y poblada a la que se le aplica el razonador.
    '''

    print(len(coincidencias))
    print(mainSubject)

    global OntoGenerada
    OntoGenerada = Ontology(world=default_world, base_iri=mainSubject + "#")

    with OntoGenerada:
        global mutex

        claseRaiz = types.new_class(mainSubject, (Thing,))
        claseRaiz.label = mainSubject
        mutex -= 1
        Enlazador.buscarURIEnlaceWordnet(mainSubject, claseRaiz)

        for keyword in keyWords:
            word = keyword["keyword"]
            clasePrincipal = types.new_class(word, (claseRaiz,))
            clasePrincipal.label = word
            keyword["clase"] = clasePrincipal
            mutex -= 1
            Enlazador.buscarURIEnlaceWordnet(word, clasePrincipal)

        for coincidencia in coincidencias:

            class_orig = coincidencia["obj"]
            class_dest = types.new_class(class_orig.name, (Thing,))
            class_dest.label = class_orig.label
            class_dest.equivalent_to.append(class_orig)

            for padre in coincidencia["padres"]:
                print(class_dest.label, "is a", padre.label)
                class_dest.is_a.append(padre)

            for hijo in coincidencia["hijos"]:
                print(hijo.label, "is a", class_dest.label)
                hijo.is_a.append(class_dest)

            mutex -= 1
            Enlazador.buscarURIEnlaceWordnet(coincidencia["labels"][0], class_dest)

            if coincidencia["nivel"] == 2:
                for keyword in keyWords:
                    word = keyword["keyword"]
                    valorSimilitudTermino = coincidencia["similitud"][word]
                    if valorSimilitudTermino >= 2:
                        clasePrincipal = keyword["clase"]
                        class_dest.is_a.append(clasePrincipal)
            elif coincidencia["nivel"] == 3:
                for referencia in coincidencia["ReferenciadoA"]:
                    class_dest.is_a.append(referencia["obj"])

    '''
    print("$$$$$$$$$$$$$$$$ FINAL $$$$$$$$$$$$$$$$$$$$")
    c = 0
    for clase in OntoGenerada.classes():
        print(clase, clase.label,clase.is_a, clase.equivalent_to)
        c += 1
    print(c)
    '''
    print("Esperando por peticiones")
    while mutex < 0:
        time.sleep(0.1)
        pass
    print("Peticiones finalizadas")
    close_world(default_world)
    return razonar()
    # return  OntoGenerada


def enlazarConceptos(nombreConceptoDbPedia, concepto):
    with OntoDbPedia:
        conceptoDbPedia = types.new_class(nombreConceptoDbPedia, (Thing,))

    with OntoGenerada:
        concepto.equivalent_to.append(conceptoDbPedia)


def continuarProceso():
    global mutex
    mutex += 1
    #print(mutex)


def razonar():
    try:
        with OntoGenerada:
            sync_reasoner()
    except Exception:
        util.printException(Exception, "Generador.razonar")

    inconsistentes = list(OntoGenerada.inconsistent_classes())
    print("Número de clases inconsistentes: " + str(len(inconsistentes)))
    for i in range(len(inconsistentes)):
        print(inconsistentes[i])

    return OntoGenerada


def closeMoK(mainSubject):
    from exploradorRecursos import AdminFuentes

    default_world = AdminFuentes.getMoK()
    default_world.get_ontology(mainSubject + "#").destroy()
    default_world.save()
#    tempWorld.ontologies.clear()
#    tempWorld.close()
