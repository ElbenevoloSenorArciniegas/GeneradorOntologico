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
        compararConOtrosTerminosBusqueda(coincidencia, keywords)
        #print(coincidencia)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    for i in range(len(coincidencias)-1):
        for j in range(i+1, len(coincidencias)):
            valorDiferencia = compararPorTablasDeSimilitud(coincidencias[i],coincidencias[j])
            print(coincidencias[i]["labels"], " _vs_ ", coincidencias[j]["labels"], " = ", valorDiferencia)
            coincidencias[i]["similitudesSintacticas"][j] = valorDiferencia
            coincidencias[j]["similitudesSintacticas"][i] = valorDiferencia
    print("$$$$$$$$$$$$$$$$")
    for coincidencia in coincidencias:
        coincidencia["promedioSimilitudes"] = sum(coincidencia["similitudesSintacticas"]) / len(coincidencia["similitudesSintacticas"])
        print(coincidencia["obj"].name, coincidencia["similitudesSintacticas"],coincidencia["promedioSimilitudes"],coincidencia["similitudAKeywords"])
    print("$$$$$$$$$$$$$$$$")
    return coincidencias
'''
#####################################################################################
'''
def compararPorTablasDeSimilitud(obj1, obj2):

    tabla = crearTabla(obj1,obj2)
    len1= len(obj1["arregloDeTerminos"])
    len2 = len(obj2["arregloDeTerminos"])

    minimos = getMinimo(tabla,len1,len2)
    minimos.extend(getMinimo(tabla,len1,len2,True))
    value = sum(minimos)/len(minimos)
    #print("Value:"+ str(value)+"\n")

    return value

def prepararArregloDeTerminos(obj):
    arr = []
    otherClasses = []
    otherLabels = []
    rtn = []
    arr.append(obj["obj"])
    arr.extend(obj["properties"])
    #Experimentalmente se ha visto que las clases suelen tener números consecutivos como nombres
    #Las propiedades y etiquetas son más confiables para comparaciones léxicas (TODO: comentarios)

    otherClasses.extend(obj["parents"])
    otherClasses.extend(obj["children"])
    #otherClasses.extend(obj["is_a"])
    # arr.extend(obj["subClasses"])

    for otherClass in otherClasses:
        #arr.append(otherClass["obj"])
        arr.extend(otherClass["properties"])
        for p in otherClass["parents"]+otherClass["children"]:
            try:
                if not p.label: pass
                else: otherLabels.extend(p.label)
            except: pass
        otherLabels.extend(otherClass["labels"])

    for x in arr:
        try:
            if not x.name: pass
            else:
                #yield x.name
                if not x.name in rtn: rtn.append(x.name)
        except:
            pass
            #Aquí están llegando Restricciones, pero no he identificado qué son, de dónde vienen y cómo puedo aprovecharlas.
            #print("[Deleted object without name]",x)

    for label in obj["labels"]+otherLabels:
        #yield label
        if not label in rtn: rtn.append(label)

    return rtn

def crearTabla(obj1,obj2):
    arr1 = obj1["arregloDeTerminos"]
    arr2 = obj2["arregloDeTerminos"]
    #textTabla = ""
    tabla = [[0 for x in range(len(arr2))] for y in range(len(arr1))]
    for i in range(len(arr1)):
        for j in range(len(arr2)):
            tabla[i][j] = getStringSimilarity(arr1[i], arr2[j]) / (obj1["similitudAKeywords"] * obj2["similitudAKeywords"])
            #textTabla += str(round(tabla[i][j], 4)) + "\t"
        #textTabla += "\n"
    #print("Tabla: ",textTabla)
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
def compararConOtrosTerminosBusqueda(obj, keywords):
    arr = obj["arregloDeTerminos"]
    mayor = 1
    for x in arr:
        x = x.lower()
        count = 0
        for word in keywords:
            word = word.lower()
            if x.find(word) > -1:
                count = count + 1
        #if(count == 0): count = 1 #Es un valor divisor en la fórmula siguiente. Es peligroso dejarlo en 0
        #obj["similitudAKeywords"].append(count)
        if count > mayor : mayor = count
    obj["similitudAKeywords"] = mayor
    #print(obj["obj"].name,obj["similitudAKeywords"])

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