import traceback
import sys
from operator import itemgetter


def printException(Exception ,msg):
    print("Exception at " + msg)
    print(traceback.format_exc())
    # or
    print(sys.exc_info()[2])


def imprimirDatosSimilitudes(arregloClases, orderBy = "similitudAKeywords", asc=True):
    arregloClases = sorted(arregloClases, key=itemgetter(orderBy), reverse=asc)

    for clase in arregloClases:
        arregloSimilitudes = dict.copy(clase["similitud"])
        for key in arregloSimilitudes:
            arregloSimilitudes[key] = round(arregloSimilitudes[key],2)

        print(arregloSimilitudes, "\t\t\t",
              round(clase["similitudAKeywords"],3), "\t\t",
              round(clase["promedioDistancias"], 3), "\t\t",
              clase["labels"][0].replace(" ", "_"))