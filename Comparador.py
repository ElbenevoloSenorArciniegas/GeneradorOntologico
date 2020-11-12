import sys


def limpiarCoincidencias(coincidencias, keywords):
    '''

    :param coincidencias:
    :param keywords:
    :return:
    \'''
    for obj in coincidencias:
        print("Children of " + str(obj["obj"]))
        for child in obj["children"]:
            try:
                print(str(child.label))
            except:
                print("No tiene label")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Parents of " + str(obj["obj"]))
        for parent in obj["parents"]:
            try:
                print(str(parent.label))
            except:
                print("No tiene label")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    '''
    #Llena e inicializa el arreglo con n ceros
    for coincidencia in coincidencias:
        coincidencia["similitudesSintacticas"] = [0 for x in range(len(coincidencias))]

    for i in range(len(coincidencias)-1):
        for j in range(i+1, len(coincidencias)):
            valorDiferencia = compararPorTablasDeSimilitud(coincidencias[i],coincidencias[j])
            coincidencias[i]["similitudesSintacticas"][j] = valorDiferencia
            coincidencias[j]["similitudesSintacticas"][i] = valorDiferencia
    print("$$$$$$$$$$$$$$$$")
    print(coincidencias[0])
    print("$$$$$$$$$$$$$$$$")
    return coincidencias

def compararPorTablasDeSimilitud(obj, obj2):

    arr1 = list(prepararArregloDeTerminos(obj))
    arr2 = list(prepararArregloDeTerminos(obj2))
    print(".-.-.-.-.-.-.-.-.--.-.-.-.-.-.-.-")
    print(arr1, "\n\t\t #-vs-#\n",arr2)
    print(".-.-.-.-.-.-.-.-.--.-.-.-.-.-.-.-")

    textTabla = ""
    tabla = [[0 for x in range(len(arr2))] for y in range(len(arr1))]
    for i in range(len(arr1)):
        for j in range(len(arr2)):
            tabla[i][j] = getStringSimilarity(arr1[i],arr2[j])
            textTabla += str(round(tabla[i][j],4))+"\t"
        textTabla += "\n"
    print("Tabla:")
    print(textTabla)

    minimos = getMinimo(tabla,len(arr1),len(arr2))
    minimos.extend(getMinimo(tabla,len(arr1),len(arr2),True))
    value = sum(minimos)/len(minimos)
    print("Value:"+ str(value)+"\n")

    return value

def prepararArregloDeTerminos(obj):
    arr = []
    arr.append(obj["obj"])
    arr.extend(obj["parents"])
    arr.extend(obj["children"])
    arr.extend(obj["properties"])
    for x in arr:
        yield x.name

def getMinimo(tabla, x,y, invertirSentido= False):
    if invertirSentido:
        temp = x
        x= y
        y = temp

    arrMin = []
    for i in range(x):
        minimo = sys.maxsize
        for j in range(y):
            if not invertirSentido:
                minimo = min(minimo, tabla[i][j])
            else:
                minimo = min(minimo, tabla[j][i])
        arrMin.append(minimo)
    return arrMin

def compararConOtrosTerminos(obj, keywords):
    return obj

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