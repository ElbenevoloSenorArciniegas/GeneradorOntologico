import sys


def limpiarCoincidencias(coincidencias, keywords, sinonimos, umbral):
    '''

    :param coincidencias:
    :param keywords:
    :return:
    '''
    #Llena e inicializa el arreglo con n ceros
    for coincidencia in coincidencias:
        coincidencia["similitudesSintacticas"] = [0 for x in range(len(keywords+sinonimos))]
        compararConOtrosTerminosBusqueda(coincidencia, keywords)
        #print(coincidencia["obj"].name,":",coincidencia["obj"].label)
        #print(coincidencia)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    for coincidencia in coincidencias:
        coincidencia["promedioSimilitudes"] = compararPorTablasDeSimilitud(coincidencia,keywords+sinonimos)

    mayor = 0
    menor = 100
    print("$$$$$$$$$$$$$$$$")
    for coincidencia in coincidencias:
        print(coincidencia["obj"].name, coincidencia["similitudesSintacticas"],coincidencia["promedioSimilitudes"],coincidencia["similitudAKeywords"])
    print("$$$$$$$$$$$$$$$$")
    
    rtn = []
    for coincidencia in coincidencias:
        if coincidencia["promedioSimilitudes"] <= mayor - (mayor-menor)*umbral/100:
            rtn.append(coincidencia)
    return rtn
'''
#####################################################################################
'''
def compararPorTablasDeSimilitud(obj, keywords):

    tabla = crearTabla(obj,keywords)
    len1= len(obj["arregloDeTerminos"])
    len2 = len(keywords)

    #for i in xrange(len2):
        #obj["similitudesSintacticas"] = 

    #minimos = getMinimo(tabla,len1,len2)
    minimos = getMinimo(tabla,len1,len2,True)
    obj["similitudesSintacticas"] = minimos
    value = sum(minimos)/len(minimos)
    #print("Value:"+ str(value)+"\n")

    return value

def crearTabla(obj, keywords):
    arr1 = obj["arregloDeTerminos"]
    arr2 = keywords
    #textTabla = ""
    tabla = [[0 for x in range(len(arr2))] for y in range(len(arr1))]
    for i in range(len(arr1)):
        for j in range(len(arr2)):
            tabla[i][j] = getStringSimilarity(arr1[i], arr2[j])
            #textTabla += str(round(tabla[i][j], 4)) + "\t"
        #textTabla += "\n"
    #print("Tabla: ",obj["labels"],arr1,arr2,"\n",textTabla)
    '''
    if obj2["obj"].name == "DOID_10154" and obj1["obj"].name == "TestResult":
        print("Tabla: ",obj1["labels"],arr1,obj2["labels"],arr2,"\n",textTabla)
    '''
    return tabla

def getMinimo(tabla, x,y, invertirSentido= False):
    if invertirSentido:
        x, y = y, x

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
def compararConOtrosTerminosBusqueda(obj, keywords, sinonimos = []):
    arr = obj["arregloDeTerminos"]
    mayor = 1
    countTotal = 0
    for termino in arr:
        countWords = 0
        for word in keywords:
            if termino.find(word) > -1:
                peso = ponderarSegunAparicion(termino,word)
                countWords += peso
                countTotal += peso
        if countWords > mayor : 
            mayor = countWords
    
    #Es un valor divisor en la fórmula siguiente. Es peligroso dejarlo en 0
    obj["similitudAKeywords"] =  mayor * (1 + countTotal/(len(arr)*len(keywords)))

    return obj

def ponderarSegunAparicion(termino, word):
    peso = 0

    if buscarRegex(termino, r"^("+word+")$"):
        peso = 1
    elif buscarRegex(termino, r"^("+word+")\w|\w("+word+")$"):
        peso = 0.75
    elif buscarRegex(termino, r"\w("+word+")\w"):
        peso = 0.5
    return peso

def buscarRegex(termino, regex):
    import re
    matches = re.finditer(regex, termino, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            #print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
            return True
    return False

'''
######################################################################################3
'''
def getStringSimilarity(str1, str2):
    '''
    Fórmula propuesta por:
    Jian, N., Hu, W., Cheng, G., & Qu, Y. (2005, October). Falcon-ao: Aligning ontologies with falcon. In Proceedings of K-CAP Workshop on Integrating Ontologies (pp. 85-91).
    '''
    ed = levenshtein(str1.lower(),str2.lower())
    #return 1/2.71828 * ed/ abs(len(str1) + len(str2) - ed)
    return ed / abs(len(str1) + len(str2) - ed)

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