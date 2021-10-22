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
            arregloSimilitudes[key] = round(arregloSimilitudes[key], 2)

        arregloImpresion.append([arregloSimilitudes,
                                 round(clase["similitudAKeywords"],2),
                                 clase["label"].replace(" ", "_")
                                 ])

    print(tabulate(arregloImpresion, headers=["KeyWords","Sim. KW", "Label"]))


def imprimirCandidatos(arregloClases, orderBy = "similitudASeleccionados", detalle=False):
    arregloClases = sorted(arregloClases, key=itemgetter(orderBy), reverse=True)
    arregloClasesImpresion = []
    for clase in arregloClases:
        arregloClasesImpresion.append([str(round(clase["similitudAKeywords"], 2))+",",
                                       str(round(clase["similitudASeleccionados"], 2))+",",
                                       clase["label"].replace(" ", "_")+","
                                       ])
    print(tabulate(arregloClasesImpresion, headers=["Sim. KW,", "Sim. Sel.,", "Label,"]))
    if(detalle):
        imprimirDetalleCandidatos(arregloClases)

def imprimirDetalleCandidatos(arregloClases):
    arregloSimilitudes = []
    arregloLabels=["Sim. KW,", "Sim. Sel.,", "Label,"]
    for clase in arregloClases:

        tablaDeRelaciones = []
        arregloReferenciadosOrden = []
        for referenciado in clase["ReferenciadoA"]:
            lblReferenciado = referenciado["label"]
            arregloReferenciadosOrden.append({ 'label': lblReferenciado , 'valor' : round(clase["similitud"][lblReferenciado], 2)})
        arregloReferenciadosOrden = sorted(arregloReferenciadosOrden, key=itemgetter('valor'), reverse=True)
        for referenciado in arregloReferenciadosOrden:
            tablaDeRelaciones.append([
                referenciado['valor'],
                referenciado['label']
            ])

        print("\n\n"+clase["label"]+":\n")
        print(tabulate(tablaDeRelaciones, headers=["Sim.","Label"]))

        #print("\n", clase["similitudesSintacticas"], "\n")

        #print(tabulate(clase["tabla"], headers=clase["tabla_arr2"]))


        auxArr = [str(round(clase["similitudAKeywords"], 2))+",",
                  str(round(clase["similitudASeleccionados"], 2))+",",
                  clase["label"].replace(" ", "_")[:10]+"," #10 primeros caracteres de la label
                  ]

        for key in clase["similitud"]:
            arregloLabels.append(key[:10]+",") #10 primeros caracteres de la label
            auxArr.append(str(round(clase["similitud"][key], 2))+",")
        arregloSimilitudes.append(auxArr)

    print("\n\nTABLA DE SIMILITUD CANDIDATOS vs SELECCIONADOS\n\n")
    print(tabulate(arregloSimilitudes, headers=arregloLabels))