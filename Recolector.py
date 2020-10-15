from owlready2 import default_world

import AdminFuentes
import Generador

def buscar(keyWords):

    #default_world = AdminFuentes.getWorld()

    # Método de búsqueda
    #articles = default_world.search(label=FTS(keyWords)) ¿Qué es FTS?
    articles = default_world.search(label=keyWords)

    for a in articles:
        print(a)

    coincidencias = []
    return Generador.generarOnto(coincidencias)