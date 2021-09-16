from util.util import imprimirDatosSimilitudes


def limpiarCoincidencias(coincidencias, keywords, umbral):
    '''

    :param coincidencias:
    :param keywords:
    :return:
    '''
    #Calcula la similitud con los términos de búsqueda y los sinónimos
    for keyword in keywords:
        word = keyword["keyword"]
        for coincidencia in coincidencias:
            valorSimilitud = ponderarPorTerminosBusqueda(coincidencia["arregloDeTerminos"], [word], keyword["sinonimos"])
            coincidencia["similitud"][word] = valorSimilitud
            coincidencia["similitudAKeywords"] += valorSimilitud
    
    #Los que tengan similitud calculada mayor a 2 se tomarán como referentes
    #Los de similitud menor o igual a 1 se descartarán
    #Los que tienen apariciones de los términos de búsqueda serán comparados contra los 
    #referentes (seleccionados) para conseguir un valor que estime qué tan similares
    #son estos conceptos intermedios a los que más se acercan a la búsqueda original.

    candidatos = []
    seleccionados = []
    for coincidencia in coincidencias:
        coincidencia["similitudAKeywords"] /= len(keywords)
        if coincidencia["similitudAKeywords"] >= 2:
            seleccionados.append(coincidencia)
        elif coincidencia["similitudAKeywords"] > 1:
            candidatos.append(coincidencia)

    print("\n\n$$$$$$$$$$$$$$$$  SELECCIONADOS   $$$$$$$$$$$$$$\n\n")
    imprimirDatosSimilitudes(seleccionados)
    terminosReferentes = []
    for seleccionado in seleccionados:
        for terminoReferente in seleccionado["arregloDeTerminos"]:
            if terminoReferente not in terminosReferentes:
                terminosReferentes.append(terminoReferente)

    #print(terminosReferentes)

    mayor = 0
    menor = 100

    for candidato in candidatos:
        #Llena e inicializa el arreglo con n ceros
        candidato["similitudesSintacticas"] = [0 for x in range(len(terminosReferentes))]
        promedioDistancias = compararPorTablasDeDistancia(candidato,terminosReferentes) / candidato["similitudAKeywords"]
        candidato["promedioDistancias"] = promedioDistancias
        if promedioDistancias > mayor: 
            mayor = promedioDistancias
        elif promedioDistancias < menor: 
            menor = promedioDistancias
    print("\n\n$$$$$$$$$$$$$$$$ CANDIDATOS $$$$$$$$$$$$$$$$$$$$$$$$$\n\n")
    imprimirDatosSimilitudes(candidatos,orderBy="promedioDistancias",asc=False)

    print("\n\n$$$$$$$$$   VALOR LÍMITE  $$$$$$$\n\n")
    rtn = seleccionados
    valorLimite = mayor - (mayor-menor)*umbral/100
    print("Mayor: ",round(mayor,3), "Menor: ",round(menor,3), "Umbral: ",round(umbral,3),"% \tValor límite: ",round(valorLimite,3))

    candidatosSeleccionados = []
    for candidato in candidatos:
        if candidato["promedioDistancias"] <= valorLimite:
            rtn.append(candidato)
            candidatosSeleccionados.append(candidato)
    print("\n\n$$$$$$$$$   CANDIDATOS SELECCIONADOS  $$$$$$$\n\n")
    imprimirDatosSimilitudes(candidatosSeleccionados,orderBy="promedioDistancias",asc=False)

    return rtn
'''
#####################################################################################
'''
def compararPorTablasDeDistancia(obj, referentes):

    tabla = crearTabla(obj,referentes)
    len1= len(obj["arregloDeTerminos"])
    len2 = len(referentes)

    #minimos = getMinimos(tabla,len1,len2)
    minimos = getMinimos(tabla,len1,len2,True)
    obj["similitudesSintacticas"] = minimos
    value = sum(minimos)/len(minimos)
    #print("Value:"+ str(value)+"\n")

    return value

def crearTabla(obj, referentes):
    arr1 = obj["arregloDeTerminos"]
    arr2 = referentes
    #textTabla = ""
    tabla = [[0 for x in range(len(arr2))] for y in range(len(arr1))]
    for i in range(len(arr1)):
        for j in range(len(arr2)):
            tabla[i][j] = getStringSimilarity(arr1[i], arr2[j])
            #textTabla += str(round(tabla[i][j], 4)) + "\t"
        #textTabla += "\n"
    #print("Tabla: ",obj["labels"],arr1,arr2,"\n",textTabla)
    return tabla

def getMinimos(tabla, x,y, invertirSentido= False):
    if invertirSentido:
        x, y = y, x

    arrMin = []
    for i in range(x):
        #Es virtualmente improbable que la diferencia de dos cadenas supere el 1000, y si así fuera y 
        #todas los términos de un objeto superaran esa diferencia, es definitivo que no va a ser un
        #resultado candidato...
        minimo = 1000 
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

def ponderarPorTerminosBusqueda(arregloDeTerminos, keywords, sinonimos):
    acumulador = 0
    contador = 1
    for termino in arregloDeTerminos:
        for word in keywords + sinonimos:
            if termino.find(word) > -1:
                peso = ponderarSegunAparicion(termino,word)
                if word in sinonimos:
                    peso /= 2
                contador += (peso >= 0.5)
                acumulador += peso
    #Es un valor divisor en la fórmula siguiente. Es peligroso dejarlo en 0
    return contador/len(keywords) * (1 + acumulador/(len(arregloDeTerminos)*len(keywords)))

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