#from owlready2 import default_world

import AdminFuentes
import Generador

def buscar(keyWords):

    default_world = AdminFuentes.getWorld()

    # Método de búsqueda
    #articles = default_world.search(label=FTS(keyWords)) ¿Qué es FTS?

    coincidencias = []
    properties = []
    '''
    #has_toppings = [] No sé qué sea topping, pero es bueno no olvidar que existe
    # has_toppings.append(onto.search(has_topping ="*" + word + "*",_case_sensitive=False))
    '''


    for word in keyWords:
        #print(word)

        for onto_key in default_world.ontologies.keys():
            #print(onto_key)
            onto = default_world.get_ontology(onto_key)

            labels = onto.search(label="*"+word+"*",_case_sensitive=False)

            #print("########################################################")
            for label in labels:
                print(str(label))
            print("########################################################")

            print("Properties")
            properties.extend(onto.properties())

            for property in properties:
                print(str(property),str(property.label),str(property.domain),str(property.comment),str(property.name))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            coincidencias.extend(labels)
            for label in labels:
                print("Children of "+str(label))
                children = onto.get_children_of(label)
                for child in children:
                    print(str(child.label))
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                print("Parents of " + str(label))
                parents = onto.get_parents_of(label)
                for parent in parents:
                    print(str(parent.label))
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

                '''
                Podría simplemente darle coincidencias.extend(onto.search(is_a=label))
                Eso admitiría los duplicados y gastaría memoria.
                Esta forma evita los duplicados y gasta procesamiento.
                Toca hacer pruebas y ver qué es más crítico para elegir bien. 
                
                ¿Esto es necesario: OntoGenerada.get_children_of()? Para escoger las cosas como si fueran
                sub-árboles donde cada raiz sea una coincidencia de keyword...
                ---
                things = onto.search(is_a=label)
                #things.extend(onto.search(**{"*"+word+"*" : "*"},_case_sensitive=False)) no ha sido útil.
                for thing in things:
                    print(thing.label, coincidencias.count(thing))
                    if coincidencias.count(thing) == 0:
                        coincidencias.append(thing)
                '''

    return Generador.generarOnto(keyWords[0],coincidencias)


def getStringSimilarity(str1, str2):
    '''
    Fórmula propuesta por:
    Jian, N., Hu, W., Cheng, G., & Qu, Y. (2005, October). Falcon-ao: Aligning ontologies with falcon. In Proceedings of K-CAP Workshop on Integrating Ontologies (pp. 85-91).
    '''
    ed = levenshtein(str1,str2)
    return 1/2.71828 * ed/ abs(len(str1) + len(str2) - ed)

def levenshtein(str1, str2):
    '''
    Devuelve la cantidad mínima de acciones de sustitución, añadido o quitada de caracteres
    para que str1 se vuelva str2.     [Casa -> calle] > cala > calla > calle : 3
    :param str1:
    :param str2:
    :return:
    '''
    d=dict()
    for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
    for i in range(len(str2)+1):
     d[0][i] = i
    for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
    return d[len(str1)][len(str2)]