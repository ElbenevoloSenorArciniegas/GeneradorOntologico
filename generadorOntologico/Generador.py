from owlready2 import close_world, Ontology, World, types, sync_reasoner_pellet, sync_reasoner
from util import util

tempWorld = World()

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

    OntoGenerada = Ontology(world=tempWorld, base_iri=mainSubject + "#")

    with OntoGenerada:
        for coincidencia in coincidencias:
            class_orig = coincidencia["obj"]
            class_dest = types.new_class(class_orig.name, (class_orig,))
            class_dest.label = class_orig.label
    '''
            print(class_orig.is_a)
            for parent in list(class_orig.is_a):
                if not isinstance(parent, Thing): class_orig.is_a.remove(parent)  # Bank node
                class_dest.is_a.append(parent)
    
        for clase in objetos:
            newClass = types.new_class(clase.name, (Thing,))
        for clase in propiedades:
            newClass = types.new_class(clase.name, (DataProperty,))
    '''

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