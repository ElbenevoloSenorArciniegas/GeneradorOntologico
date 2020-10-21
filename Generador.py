import os
import AdminFuentes
from owlready2 import *

PATH = AdminFuentes.PATH

def generarOnto(mainSubject, coincidencias):
    #algoritmo de mezclar

    text = ""
    for label in coincidencias:
        text += str(label) + " : " + str(label.label) + "\n"
    print(text)

    OntoGenerada = get_ontology(PATH + "OntoGenerada.owl")
    OntoGenerada.load()
    OntoGenerada.base_iri = mainSubject + "#"

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
    return "Razonador dice: "+ str(OntoGenerada)
