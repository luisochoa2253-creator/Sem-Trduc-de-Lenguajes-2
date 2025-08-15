def detectar_(frase):
    elementos = frase.split()
    for elem in elementos:
        if elem.isdigit():
            print(f"{elem} tiene un valor entero")
        else:
            try:
                float_ = float(elem)
                if '.' in elem:
                    print(f"{elem} tiene un valor flotante")
                else:
                    print(f"{elem} tiene un valor entero")
            except ValueError:
                print(f"{elem} es una cadena")

frase = input("Ingresa una frase con numeros enteros, flotantes y cadenas: ")
detectar_(frase)