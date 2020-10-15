import sys, os
from owlready2 import default_world

PATH = os.path.relpath('sources') +"/"

def getWorld():
    try:
        default_world.set_backend(filename=PATH + "World.sqlite3")
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

'''
    Estoy seguro de cómo cerrar el mundo, pero ni idea de volver a abrirlo. Queda como objeto de pruebas para 
    cuando esté usándose en simultáneo. No sé qué tan malo sea dejarlo abierto por siempre.
'''


def addFuenteLocal(file_name):
    try:
    # ¿Necesito trabajar con ontologías importadas o las cargo directamente en el world?
    # tipo myWorld.get_ontology(ruta).load()    que de por sí ya se hace...
    # baseOnto = myWorld.get_ontology("BASE_ONTO_PATH").imported_ontologies.append(myWorld.get_ontology(file_name).load())

        getWorld()

        default_world.get_ontology(PATH + file_name).load()
        default_world.save()
        #default_world.close()
        return "Success:"

    except IOError as e:
        return "IOError at Admin.addFuenteLocal: " + str(e)
    except:
        return "Failed at Admin.addFuenteLocal: " + str(sys.exc_info()[0])
    '''
    finally:
        try:
            default_world.close()
        except:
            return "Error closing default_world"
    '''

def addFuenteExterna(IRI):
    try:
        getWorld()
        # Lo mismo de arriba
        default_world.get_ontology(IRI).load()
        default_world.save()
        return "Success"
    except IOError as e:
        return "IOError at Admin.addFuenteExterna: " + str(e)
    except:
        return "Failed at Admin.addFuenteExterna: " + str(sys.exc_info()[0])
    '''
        finally:
            try:
                default_world.close()
            except:
                return "Error closing default_world"
    '''


def removeFuente(IRI):
    try:
        getWorld()
        # remover
        #print(myWorld.get_ontology(IRI))
        default_world.get_ontology(IRI).destroy()
        default_world.save()
        return "Success"
    except IOError as e:
        return "IOError at Admin.removeFuente: " + str(e)
    except:
        return "Failed at Admin.removeFuente: " + str(sys.exc_info()[0])
    '''
        finally:
            try:
                default_world.close()
            except:
                return "Error closing default_world"
        '''


def listarKeysWorld():
    try:
        getWorld()
        keys = ""
        for key in default_world.ontologies.keys():
            keys += key + "<br> "
        #default_world.close()
        return "Fuentes cargadas actualmente en el mundo:<br>" + keys
    except:
        return "Failed at Admin.listarKeysWorld: " + str(sys.exc_info()[0])