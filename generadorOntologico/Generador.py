from owlready2 import close_world, Ontology, World, types, sync_reasoner_pellet, sync_reasoner, set_log_level

from exploradorRecursos import AdminFuentes
from util import util
set_log_level(9)

tempWorld = World()
default_world = AdminFuentes.getMoK()

def generarOnto(mainSubject, coincidencias):
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
        for coincidencia in coincidencias:
            class_orig = coincidencia["obj"]
            class_dest = types.new_class(class_orig.name, (class_orig,))
            class_dest.label = class_orig.label

    #for i in tempWorld.graph.execute("SELECT * FROM quads where s=322 or p=322 or o=322 or d=322"):
    #    print(i)

    c = 0
    for clase in OntoGenerada.classes():
        print(clase, clase.label,clase.is_a)
        c += 1
    print(c)

    #pass
    close_world(OntoGenerada)
    return razonar(OntoGenerada)

def razonar(OntoGenerada):
    try:
        with OntoGenerada:
            sync_reasoner()
            #sync_reasoner_pellet()
            # sync_reasoner_pellet(infer_property_values=True)
            # sync_reasoner(infer_property_values=True)
            #list(tempWorld.inconsistent_classes())
    except Exception:
        util.printException(Exception, "Generador.razonar")

    inconsistentes = list(tempWorld.inconsistent_classes())
    print("Número de clases inconsistentes: "+ str(len(inconsistentes)))
    for i in range(len(inconsistentes)):
        print(inconsistentes[i])

    return OntoGenerada



def closeMoK(mainSubject):
    from exploradorRecursos import AdminFuentes

    default_world = AdminFuentes.getMoK()
    default_world.get_ontology(mainSubject+"#").destroy()
    default_world.save()
    tempWorld.ontologies.clear()
#    tempWorld.close()