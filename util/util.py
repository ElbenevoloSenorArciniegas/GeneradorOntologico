import traceback
import sys
from operator import itemgetter
from tabulate import tabulate


def printException(Exception ,msg):
    print("Exception at " + msg)
    print(traceback.format_exc())
    # or
    print(sys.exc_info()[2])


def imprimirSeleccionados(arregloClases, orderBy = "similitudAKeywords"):
    arregloClases = sorted(arregloClases, key=itemgetter(orderBy), reverse=True)
    arregloImpresion = []
    for clase in arregloClases:
        arregloSimilitudes = dict.copy(clase["similitud"])
        for key in arregloSimilitudes:
            arregloSimilitudes[key] = round(arregloSimilitudes[key], 3)

        arregloImpresion.append([arregloSimilitudes,
                                 round(clase["similitudAKeywords"],3),
                                 clase["labels"][0].replace(" ", "_")
                                 ])

    print(tabulate(arregloImpresion, headers=["KeyWords","Sim. KW", "Label"]))


def imprimirCandidatos(arregloClases, orderBy = "similitudASeleccionados", detalle=False):
    arregloClases = sorted(arregloClases, key=itemgetter(orderBy), reverse=True)
    arregloClasesImpresion = []
    arregloSimilitudes = []
    llenarLabels = True
    arregloLabels=["Sim. KW", "Sim. Sel.", "Label"]
    for clase in arregloClases:
        if detalle:
            auxArr = [round(clase["similitudAKeywords"], 3),
                      round(clase["similitudASeleccionados"], 3),
                      clase["labels"][0].replace(" ", "_")[:10] #10 primeros caracteres de la label
                      ]

            for key in clase["similitud"]:
                if llenarLabels:
                    arregloLabels.append(key[:10]) #10 primeros caracteres de la label
                auxArr.append(round(clase["similitud"][key], 3))
            arregloSimilitudes.append(auxArr)

        arregloClasesImpresion.append([round(clase["similitudAKeywords"], 3),
                                       round(clase["similitudASeleccionados"], 3),
                                       clase["labels"][0].replace(" ", "_")
                                       ])

    print(tabulate(arregloClasesImpresion, headers=["Sim. KW", "Sim. Sel.", "Label"]))
    if detalle:
        print("\n\nTABLA DE SIMILITUD CANDIDATOS vs SELECCIONADOS\n\n")
        print(tabulate(arregloSimilitudes, headers=arregloLabels))