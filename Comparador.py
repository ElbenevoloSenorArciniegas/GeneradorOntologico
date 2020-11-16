import sys


def limpiarCoincidencias(coincidencias, keywords):
    '''

    :param coincidencias:
    :param keywords:
    :return:
    '''
    #Llena e inicializa el arreglo con n ceros
    for coincidencia in coincidencias:
        coincidencia["similitudesSintacticas"] = [0 for x in range(len(coincidencias))]
        coincidencia["arregloDeTerminos"] = prepararArregloDeTerminos(coincidencia)

    for i in range(len(coincidencias)-1):
        for j in range(i+1, len(coincidencias)):
            valorDiferencia = compararPorTablasDeSimilitud(coincidencias[i],coincidencias[j])
            coincidencias[i]["similitudesSintacticas"][j] = valorDiferencia
            coincidencias[j]["similitudesSintacticas"][i] = valorDiferencia
    print("$$$$$$$$$$$$$$$$")
    for coincidencia in coincidencias:
        coincidencia["promedioSimilitudes"] = sum(coincidencia["similitudesSintacticas"]) / len(coincidencia["similitudesSintacticas"])
        compararConOtrosTerminos(coincidencia, keywords)
        print(coincidencia["obj"].name, coincidencia["similitudesSintacticas"],coincidencia["promedioSimilitudes"],coincidencia["similitudAKeywords"])
    print("$$$$$$$$$$$$$$$$")
    return coincidencias
'''
#####################################################################################
'''
def compararPorTablasDeSimilitud(obj, obj2):

    arr1 = obj["arregloDeTerminos"]
    arr2 = obj2["arregloDeTerminos"]
    ''' 
    print(".-.-.-.-.-.-.-.-.--.-.-.-.-.-.-.-")
    print(arr1, "\n\t\t #-vs-#\n",arr2)
    print(".-.-.-.-.-.-.-.-.--.-.-.-.-.-.-.-")
    '''
    tabla = crearTabla(arr1,arr2)

    minimos = getMinimo(tabla,len(arr1),len(arr2))
    minimos.extend(getMinimo(tabla,len(arr1),len(arr2),True))
    value = sum(minimos)/len(minimos)
    #print("Value:"+ str(value)+"\n")

    return value

def prepararArregloDeTerminos(obj, abbleToGoDeeper = True):
    arr = []
    rtn = []
    #arr.append(obj["obj"])
    #Experimentalmente se ha visto que las clases suelen tener números consecutivos como nombres
    #Las propiedades y etiquetas son más confiables para comparaciones léxicas (TODO: comentarios en un futuro)
    arr.extend(obj["parents"])
    arr.extend(obj["children"])
    arr.extend(obj["is_a"])
    # arr.extend(obj["subClasses"])
    #print(obj, abbleToGoDeeper,"\n",arr)
    if(abbleToGoDeeper):
        for x in arr:
            rtn.extend(list(prepararArregloDeTerminos(x, False)))
    else:
        arr.extend(obj["properties"])
        for x in arr:
            try:
                if not x.name: pass
                else: rtn.extend(x.name)
            except:
                pass
                #Aquí están llegando Restricciones, pero no he identificado qué son, de dónde vienen y cómo puedo aprovecharlas.
                #print("[Deleted object without name]",x)
    for label in obj["labels"]:
        rtn.extend(label)
    print(abbleToGoDeeper, rtn)
    return rtn

def crearTabla(arr1,arr2):
    #textTabla = ""
    tabla = [[0 for x in range(len(arr2))] for y in range(len(arr1))]
    for i in range(len(arr1)):
        for j in range(len(arr2)):
            tabla[i][j] = getStringSimilarity(arr1[i], arr2[j])
            #textTabla += str(round(tabla[i][j], 4)) + "\t"
        #textTabla += "\n"
    # print("Tabla:")
    # print(textTabla)
    return tabla

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

'''
######################################################################################3
'''
def compararConOtrosTerminos(obj, keywords):
    arr = obj["arregloDeTerminos"]
    count = 0
    for x in arr:
        x = x.lower()
        for word in keywords:
            word = word.lower()
            if x.find(word) > -1:
                count = count + 1
    obj["similitudAKeywords"].append(count / (len(keywords)*len(arr)))
    '''
    for word in keywords:
        word = word.lower()
        count = 0
        for x in arr:
            x = x.lower()
            if x.find(word) > -1 :
                count = count + 1
        obj["similitudAKeywords"].append(count / len(arr))

    for i in range(len(keywords)-1):
        word = keywords[i].lower()
        for j in range(i+1,len(keywords)):
            word2 = keywords[j].lower()
            count = 0
            for x in arr:
                x = x.lower()
                if x.find(word) > -1 and x.find(word2) > -1:
                    count = count + 10
            obj["similitudAKeywords"].append(count/len(arr))
    print("///////////////////////////////")
    tabla = crearTabla(keywords, arr )
    for i in range(len(keywords)):
        obj["similitudAKeywords"].append(min(tabla[i]))
    #print(obj,tabla)
    #print("///////////////////////////////")
    '''
    return obj
'''
######################################################################################3
'''
def getStringSimilarity(str1, str2):
    '''
    Fórmula propuesta por:
    Jian, N., Hu, W., Cheng, G., & Qu, Y. (2005, October). Falcon-ao: Aligning ontologies with falcon. In Proceedings of K-CAP Workshop on Integrating Ontologies (pp. 85-91).
    '''
    ed = levenshtein(str1.lower(),str2.lower())
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