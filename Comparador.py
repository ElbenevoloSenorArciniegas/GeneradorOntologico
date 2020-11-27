import sys


def limpiarCoincidencias(coincidencias, keywords, sinonimos, umbral):
    '''

    :param coincidencias:
    :param keywords:
    :return:
    '''
    #Calcula la similitud con los términos de búsqueda y los sinónimos
    coincidencias = ponderarPorBusqueda(coincidencias, keywords, sinonimos)
    
    #Los que tengan similitud calculada mayor a 2 se tomarán como referentes
    #Los de similitud menor o igual a 1 se descartarán
    #Los que tienen apariciones de los términos de búsqueda serán comparados contra los 
    #referentes (más cercanos) para conseguir un valor que estime qué tan similares
    #son estos conceptos intermedios a los que más se acercan a la búsqueda original.

    cercanos = []
    masCercanos = []
    for coincidencia in coincidencias:
        if coincidencia["similitudAKeywords"] > 2:
            masCercanos.append(coincidencia)
        elif coincidencia["similitudAKeywords"] > 1:
            cercanos.append(coincidencia)
    
    terminosReferentes = []
    for referente in masCercanos:
        for terminoReferente in referente["arregloDeTerminos"]:
            if terminoReferente not in terminosReferentes:
                terminosReferentes.append(terminoReferente)
    print(terminosReferentes)

    mayor = 0
    menor = 100
    print("$$$$$$$$$$$$$$$$")
    for cercano in cercanos:
        #Llena e inicializa el arreglo con n ceros
        cercano["similitudesSintacticas"] = [0 for x in range(len(terminosReferentes))]
        promedioSimilitudes = compararPorTablasDeSimilitud(cercano,terminosReferentes) / cercano["similitudAKeywords"]
        cercano["promedioSimilitudes"] = promedioSimilitudes
        if promedioSimilitudes > mayor: 
            mayor = promedioSimilitudes
        elif promedioSimilitudes < menor: 
            menor = promedioSimilitudes
        print(cercano["labels"][0].replace(" ","_"), cercano["similitudesSintacticas"],cercano["promedioSimilitudes"],cercano["similitudAKeywords"])
    print("$$$$$$$$$$$$$$$$")
    
    rtn = masCercanos
    valorLimite = mayor - (mayor-menor)*umbral/100
    print(valorLimite)
    for cercano in cercanos:
        if cercano["promedioSimilitudes"] <= valorLimite:
            rtn.append(cercano)
    return rtn
'''
#####################################################################################
'''
def compararPorTablasDeSimilitud(obj, keywords):

    tabla = crearTabla(obj,keywords)
    len1= len(obj["arregloDeTerminos"])
    len2 = len(keywords)

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
def ponderarPorBusqueda(coincidencias, keywords, sinonimos):
    for coincidencia in coincidencias:
        compararConOtrosTerminosBusqueda(coincidencia, keywords, sinonimos)
    return coincidencias

def compararConOtrosTerminosBusqueda(obj, keywords, sinonimos):
    arr = obj["arregloDeTerminos"]
    mayor = 1
    countTotal = 0
    countWords = 1
    for termino in arr:
        for word in keywords + sinonimos:
            if termino.find(word) > -1:
                peso = ponderarSegunAparicion(termino,word)
                if word in sinonimos:
                    peso /= 2
                countWords += (peso >= 0.5)
                countTotal += peso
    #Es un valor divisor en la fórmula siguiente. Es peligroso dejarlo en 0
    obj["similitudAKeywords"] =  countWords/len(keywords) * (1 + countTotal/(len(arr)*len(keywords)))

    return obj

def ponderarSegunAparicion(termino, word):
    peso = 0.25

    if buscarRegex(termino, r"^("+word+")$|^("+word+")\W|\W("+word+")$|\W("+word+")\W"):
        peso = 1
    elif buscarRegex(termino, r"^("+word+")\w|\w("+word+")$"):
        peso = 0.5
    #elif buscarRegex(termino, r"\w("+word+")\w"):
        #peso = 0.25
    return peso

def buscarRegex(termino, regex):
    import re
    matches = list(re.finditer(regex, termino, re.MULTILINE))
    return len(matches) > 0
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