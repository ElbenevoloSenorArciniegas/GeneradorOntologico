
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
    return coincidencias

def compararPorTablasDeSimilitud(obj, obj2):
    return obj

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