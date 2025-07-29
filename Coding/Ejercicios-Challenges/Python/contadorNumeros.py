#Se encarga de verificar número por numero para catalogarlos pos, neg. o 0
def contador(L):
    #contadores
    negativos = 0
    positivos = 0
    ceros = 0
    if type(L) != list:
        raise Exception ("El formato de la lista es inválido")
    else:
        for i in L:
            if i > 0:
                positivos +=1 #suma uno al contador
            elif i < 0:
                negativos +=1 #suma uno al contador
            else:
                ceros +=1 #suma uno al contador
    #Resultados
    print ("La cantidad de ceros es: ", ceros)
    print ("La canridad de positivos es: ", positivos)
    print ("La cantidad de negativos es: ", negativos)
#Funcion principal, se encarga de recolectar la lista con los números
def main():
    lista = []
    #Se ejecutara siempre y cuando el usuario escriba s o S
    while True:
        numero = int(input("Ingrese el número: "))
        lista.append(numero)
        decision = str(input("Desea continuar? S/N: "))
        #Si el usuario escribe n, ejecuta contador() y termina.
        if decision.upper() == "N":
            contador(lista)
            break
            

if __name__ == "__main__":
    main()

