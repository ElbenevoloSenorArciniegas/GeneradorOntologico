

def generarOnto(coincidencias):
    #algoritmo de mezclar

    text = ""
    for set in coincidencias:
        for label in set:
            text += str(label) + "<br>"

    OntoGenerada = "OntoGenerada:<br>"+text

    return razonar(OntoGenerada)

def razonar(OntoGenerada):
    return "Razonador dice: "+ OntoGenerada
