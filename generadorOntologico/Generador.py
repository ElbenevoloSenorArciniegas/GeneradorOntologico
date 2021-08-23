from owlready2 import close_world, Ontology, types, sync_reasoner, set_log_level, Thing

from exploradorRecursos import AdminFuentes
from generadorOntologico import Enlazador
from util import util
set_log_level(9)

#tempWorld = World()
default_world = AdminFuentes.getMoK()

def generarOnto(mainSubject, keyWords, coincidencias):
    '''
    :param mainSubject: El tema que se usará como id de la ontología
    :param coincidencias: Arreglo de objetos seleccionados en la búsqueda, que poblarán la ontología.
    :return: OntoGenerada:  Ontología generada y poblada a la que se le aplica el razonador.
    '''

    #for coincidencia in coincidencias:
        #print(str(coincidencia["obj"])," : ",str(coincidencia["obj"].label))
    print(len(coincidencias))

    print(mainSubject)

    OntoGenerada = Ontology(world=default_world, base_iri=mainSubject + "#")

    with OntoGenerada:
        claseRaiz = types.new_class(mainSubject, (Thing,))
        claseRaiz.label = mainSubject

        for keyword in keyWords:
            word = keyword["keyword"]
            clasePrincipal = types.new_class(word, (claseRaiz,))
            clasePrincipal.label = word
            keyword["clase"] = clasePrincipal

        for coincidencia in coincidencias:
            class_orig = coincidencia["obj"]
            class_dest = types.new_class(class_orig.name, (class_orig,))
            class_dest.label = class_orig.label

            conceptoDbPedia = Enlazador.buscarURIEnlaceWordnet(coincidencia["labels"][0])
            if conceptoDbPedia is not None:
                class_dest.equivalent_to.append(conceptoDbPedia)

            for keyword in keyWords:
                word = keyword["keyword"]
                valorSimilitudTermino = coincidencia["similitud"][word]
                if valorSimilitudTermino >= 2:
                    clasePrincipal = keyword["clase"]
                    class_dest.is_a.append(clasePrincipal)


    c = 0
    for clase in OntoGenerada.classes():
        print(clase, clase.label,clase.is_a, clase.equivalent_to)
        c += 1
    print(c)

    #pass
    close_world(OntoGenerada)
    return razonar(OntoGenerada)

def razonar(OntoGenerada):
    try:
        with OntoGenerada:
            sync_reasoner()
    except Exception:
        util.printException(Exception, "Generador.razonar")

    inconsistentes = list(OntoGenerada.inconsistent_classes())
    print("Número de clases inconsistentes: "+ str(len(inconsistentes)))
    for i in range(len(inconsistentes)):
        print(inconsistentes[i])

    return OntoGenerada



def closeMoK(mainSubject):
    from exploradorRecursos import AdminFuentes

    default_world = AdminFuentes.getMoK()
    default_world.get_ontology(mainSubject+"#").destroy()
    default_world.save()
#    tempWorld.ontologies.clear()
#    tempWorld.close()