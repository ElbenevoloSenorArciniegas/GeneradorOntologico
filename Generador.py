

def generarOnto(coincidencias):
    #algoritmo de mezclar

    text = ""
    for label in coincidencias:
        text += str(label) + " : " + str(label.label) + "<br>"

    OntoGenerada = "OntoGenerada:<br>"+text

    return razonar(OntoGenerada)

def razonar(OntoGenerada):
    return "Razonador dice: "+ OntoGenerada
