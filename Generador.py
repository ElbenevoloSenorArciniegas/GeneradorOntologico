import os
import AdminFuentes
from owlready2 import *

PATH = AdminFuentes.PATH
tempWorld = World()

def generarOnto(mainSubject, coincidencias):
    '''
    :param mainSubject: El tema que se usará como id de la ontología
    :param coincidencias: Arreglo de objetos seleccionados en la búsqueda, que poblarán la ontología.
    :return: OntoGenerada:  Ontología generada y poblada a la que se le aplica el razonador.
    '''

    text = ""
    for label in coincidencias:
        text += str(label) + " : " + str(label.label) + "\n"
    print(text)


    OntoGenerada = Ontology(world=tempWorld, base_iri=mainSubject + "#")

    with OntoGenerada:
        for class_orig in coincidencias:
            class_dest = types.new_class(class_orig.name, (Thing,))
            class_dest.label = class_orig.label
            for parent in list(class_orig.is_a):
                if not isinstance(parent, Thing): class_orig.is_a.remove(parent)  # Bank node
                class_dest.is_a.append(parent)
    '''
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

    return razonar(OntoGenerada)

def razonar(OntoGenerada):
    try:
        with OntoGenerada:
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    except:
        print("Exception at Razonar in Generador")
    return OntoGenerada

def cleanTempWorld():
    tempWorld.ontologies.clear()
#    tempWorld.close()