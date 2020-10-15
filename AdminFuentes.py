import sys
from owlready2 import World

PATH = "f:/Universidad/proyecto de grado/Proyecto/sources/"
BASE_ONTO_PATH = PATH + "Base-onto.owl"


# ¿Path o IRI de la base_onto?

def getWorld():
    try:
        myWorld = World(filename=PATH + "quadstore.sqlite3")
        return myWorld
    except IOError as e:
        return "IOError at Admin.getWorld: " + str(e)
    except:
        return "Failed at Admin.getWorld: " + str(sys.exc_info()[0])


'''
¿Qué pasa cuando un usuario está sacando info y tiene el mundo abierto
y se necesita añadir o eliminar alguna fuente?
¿Es necesario manejar el archivo de forma sincrónica? ¿Cómo sé cuando otra instancia está accediendo a él?
¿Cómo hago un re intentador para que espere un poquito mientras se desocupa el mundo?
'''


def addFuenteLocal(file_name):
    myWorld = getWorld()
    try:
        # ¿Necesito trabajar con ontologías importadas o las cargo directamente en el world?
        # tipo myWorld.get_ontology(ruta).load()    que de por sí ya se hace...
        # baseOnto = myWorld.get_ontology("BASE_ONTO_PATH").imported_ontologies.append(myWorld.get_ontology(file_name).load())
        myWorld.get_ontology(PATH + file_name).load()
        myWorld.save()
        #print(listarKeysWorld(myWorld))
        return "Success:"
    except IOError as e:
        return "IOError at Admin.addFuenteLocal: " + str(e)
    except:
        return "Failed at Admin.addFuenteLocal: " + str(sys.exc_info()[0])
    finally:
        myWorld.close()


def addFuenteExterna(IRI):
    myWorld = getWorld()
    try:
        # Lo mismo de arriba
        myWorld.get_ontology(IRI).load()
        myWorld.save()
        return "Success"
    except IOError as e:
        return "IOError at Admin.addFuenteExterna: " + str(e)
    except:
        return "Failed at Admin.addFuenteExterna: " + str(sys.exc_info()[0])
    finally:
        myWorld.close()


def removeFuente(IRI):
    myWorld = getWorld()
    try:
        # remover
        myWorld.get_ontology(IRI).destroy()
        myWorld.save()
        return "Success"
    except IOError as e:
        return "IOError at Admin.removeFuente: " + str(e)
    except:
        return "Failed at Admin.removeFuente: " + str(sys.exc_info()[0])
    finally:
        myWorld.close()


def listarKeysWorld(myWorld=getWorld()):
    keys = ""
    for key in myWorld.ontologies.keys():
        keys += key + "<br> "
    myWorld.close()
    return "Fuentes cargadas actualmente en el mundo:<br>" + keys
