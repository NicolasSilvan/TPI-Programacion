import csv
import os

NOMBRE_ARCHIVO = "paises.csv"

#uso input() para que el usuario tenga que presionar enter luego de cada print
#para que pueda leer toda la informacion sin que lo tape el menu

def obtener_paises():

    paises = []

    if not os.path.exists(NOMBRE_ARCHIVO): #verifico que el archivo exista, si no existe lo creo
        with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"]) #seteo los nombres de los headers
            escritor.writeheader() #con esta linea creo los headers
            return paises #devuelvo la lista con la info del archivo vacia

    with open(NOMBRE_ARCHIVO, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            paises.append({"nombre": fila["nombre"], "poblacion": int(fila["poblacion"]), "superficie": int(fila["superficie"]), "continente": fila["continente"]}) #con esto agrego la info del archivo a la lista

        return paises #devuelvo la lista con la info del archivo cargada

def mostrar_catalogo():
    print("=== Libros en Stock ===")
    stock = obtener_catalogo() #llamo a la funcion que carga la info en el archivo
    
    for titulo in stock:
        print(f"TITULO : {titulo["TITULO"]} - CANTIDAD : {titulo["CANTIDAD"]}") #muestro cada titulo de manera ordenada 
    
    input()

def existe_pais(pais):
    paises_archivo = obtener_paises()

    for paises in paises_archivo: #recorro la lista de paises y checkeo que el pais ingresado exista
        if paises["nombre"].lower() == pais.lower():
            return True
        
    return False

def validar_poblacion_superficie(poblacion_superficie):
    if not poblacion_superficie.isdigit():
        return False
    
    if int(poblacion_superficie) <= 0:
        return False
    
    return True

def validar_continente(continente):
    continentes = ["america", "europa", "asia", "africa", "oceania", "antartida"] #seteo una lista con todos los continentes existentes

    if not continente or not continente.strip(): #valido que el parametro continente no este vacio
        return False

    return continente.lower() in continentes #si el continente ingresado existe dentro de la lista, devuelve True, caso contrario devuelve False

def agregar_pais(pais): #esta funcion agrega paises nuevos sin sobreescribir el archivo
    with open(NOMBRE_ARCHIVO, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"])
        escritor.writerow(pais)

def ingresar_pais():
    print("=== Ingresar Pais ===")

    paises_a_ingresar = int(input("Cuantos paises desea ingresar? "))

    for i in range(paises_a_ingresar):
        pais = input("Ingrese el nombre del pais: ")

        if existe_pais(pais): #valido que el pais ingresado no exista
            print(f"El pais {pais} ya existe en el archivo.")
            input()
            return
        
        poblacion = input("Ingrese la poblacion total del pais: ").strip()

        if not validar_poblacion_superficie(poblacion): #valido que la poblacion/superficie no sea 0 ni negativa
            print("El numero de poblacion no es valido! Debe ingresar un valor mayor que 0.")
            input()
            return
        
        poblacion = int(poblacion)

        superficie = input("Ingrese la superficie en KM2 total del pais: ").strip()

        if not validar_poblacion_superficie(superficie): #valido que la poblacion/superficie no sea 0 ni negativa
            print("El numero de superficie no es valido! Debe ingresar un valor mayor que 0.")
            input()
            return
        
        superficie = int(superficie)

        continente = input("Ingrese el continente donde se ubica el pais: ").strip()

        if not validar_continente(continente): #valido que el continente exista o no sea vacio
            print("El continente ingresado no existe o esta vacio! Debe ingresar un continente valido.")
            input()
            return

        agregar_pais({"nombre": pais, "poblacion": poblacion, "superficie": superficie, "continente": continente})

        print(f"El pais {pais} se agrego al archivo con los siguientes datos:") #Muestro de manera ordenada todos los datos ingresados al archivo
        print(f"== Poblacion : {poblacion}\t==")
        print(f"== Superficie : {superficie}\t==")
        print(f"== Continente : {continente}\t ==")
        input()
    

def guardar_paises(pais): #sobreescribo la informacion del archivo, y creo los headers de nuevo
    with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"])
        escritor.writeheader()
        escritor.writerow(pais)

def devolucion():
    titulo = input("Ingrese el nombre del titulo a devolver: ")

    if not titulo: #valido que el titulo no este vacio
        print("El titulo no puede estar vacio!")
        input()
        return
    
    catalogo = obtener_catalogo()

    for titulos in catalogo:
        if titulos["TITULO"].lower() == titulo.lower(): #busco que exista el titulo adentro del catalogo
            cantidad = input("Ingrese la cantidad de ejemplares a devolver: ")

            if not validar_cantidad(cantidad): #valido que la cantidad no sea 0 o negativo
                print("La cantidad no es valida!")
                input()
                return
            
            titulos["CANTIDAD"] += int(cantidad) #le sumo la cantidad al indice

            guardar_titulos(catalogo)
            print("Titulo devuelto correctamente!")
            input()
            
            break
    else:
        print(f"El titulo {titulo} no se ha encontrado!")
        input()


def prestamo():
    titulo = input("Ingrese el nombre del titulo a prestar: ")

    if not titulo:
        print("El titulo no puede estar vacio!")
        input()
        return
    
    catalogo = obtener_catalogo()

    for titulos in catalogo:
        if titulos["TITULO"].lower() == titulo.lower(): #busco que exista el titulo adentro del catalogo
            cantidad = input("Ingrese la cantidad de ejemplares a prestar: ")

            if not validar_cantidad(cantidad): #valido que la cantidad no sea 0 o negativo
                print("La cantidad no es valida!")
                input()
                return
            
            if titulos["CANTIDAD"] == 0:
                print("No quedan mas ejemplares de este titulo en stock!")
                input()
                break

            if (titulos["CANTIDAD"] - int(cantidad)) < 0:
                print("No puede llevarse mas titulos de los que hay en stock!")
                input()
                break

            titulos["CANTIDAD"] -= int(cantidad) #le resto la cantidad al indice

            guardar_titulos(catalogo)
            print("Titulo prestado correctamente!")
            input()
            
            break
    else:
        print(f"El titulo {titulo} no se ha encontrado!")
        input()

def actualizar_ejemplares():
    
    devo_presta = input("Es una devolucion (D) o un prestamo (P): (D/P)").strip()
    
    match devo_presta.upper(): #hago un match case para las dos opciones (prestamo/devolucion)
        case "D":
            devolucion()
        case "P":
            prestamo()
        case _:
            print("Opcion invalida!")
            input()
            return

def actualizar_poblacion_superficie():
    print("=== ACTUALIZAR POBLACION Y SUPERFICIE ===")
    pais_nombre = input("Ingrese el nombre del pais a actualizar: ")

    if not pais_nombre: #valido que el pais no este vacio
        print("El pais no puede estar vacio!")
        input()
        return
    
    paises = obtener_paises()

    for pais in paises:
        if pais["nombre"].lower() == pais_nombre.lower(): #busco que exista el pais adentro del archivo

            print("=================================================================") #muestro los datos actuales del pais a modificar
            print(f"Poblacion total actual de {pais_nombre} = {pais["poblacion"]}")
            print(f"Superficie total en KM2 actual de {pais_nombre} = {pais["superficie"]}")

            pobla_super = input("Desea actualizar la poblacion(P) o la superficie(S)? (P/S): ").strip()

            match pobla_super.lower(): #uso un match case para actualizar la superficie o la poblacion
                case "p": #poblacion
                    poblacion = input("Ingrese el numero de poblacion a actualizar: ")

                    if not validar_poblacion_superficie(poblacion): #valido que la poblacion no sea 0 o negativo
                        print("La poblacion no es valida!")
                        input()
                        return
                    
                    pais["poblacion"] = int(poblacion) #le asigno el nuevo numero de poblacion al archivo

                    guardar_paises(pais)
                    print("Ejemplares actualizados!")
                    input()
                case "s": #superficie
                    superficie = input("Ingrese el numero de superficie en KM2 a actualizar: ")

                    if not validar_poblacion_superficie(superficie): #valido que la superficie no sea 0 o negativo
                        print("La superficie no es valida!")
                        input()
                        return
                    
                    pais["superficie"] = int(superficie) #le asigno el nuevo numero de superficie al archivo
                
                    guardar_paises(pais)
                    print("Ejemplares actualizados!")
                    input()
                case _:
                    print("Opcion invalida!")
                    return
            
            break

def consultar_stock():
    titulo = input("Ingrese el nombre del titulo a consultar: ")

    if not titulo: #valido que el titulo no este vacio
        print("El titulo no puede estar vacio!")
        input()
        return
    
    catalogo = obtener_catalogo()

    for titulos in catalogo:
        if titulos["TITULO"].lower() == titulo.lower():
            print(f"TITULO : {titulos["TITULO"]} - CANTIDAD : {titulos["CANTIDAD"]}")
            input()
            break

def consultar_agotados():
    catalogo = obtener_catalogo()

    for titulos in catalogo:
        if titulos["CANTIDAD"] == 0: #recorro la lista de catalogo buscando los que tengan CANTIDAD = 0
            print("=== Titulos sin stock ===")
            print(f"TITULO : {titulos["TITULO"]}")
            input()
            break
    else:
        print("No se encontraron titulos agotados!")
        input()

def mostrar_menu():
    opcion = ""
    while opcion != 87: #mientras la opcion no sea 7 el programa va a seguir ejecutandose
        print("\n==== MENU PAISES ====")
        print("1) Ingresar pais")
        print("2) Actualizar datos de poblacion y superficie")
        print("3) Buscar pais")
        print("4) Filtrar paises (Continente/Rango poblacion/Rango Superficie)")
        print("5) Ordenar paises (Nombre/Poblacion/Superficie)")
        print("6) Mostrar estadisticas")
        print("7) Salir")

        opcion = input("Ingrese una opcion: ").strip()

        match opcion:
            case "1":
                ingresar_pais() 
            case "2":
                actualizar_poblacion_superficie()
            case "3":
                mostrar_catalogo() 
            case "4":
                consultar_stock()
            case "5":
                consultar_agotados()
            case "6":
                ingresar_pais()
            case "7":
                print("Gracias por usar nuestro programa!")
                input()
                break
            case _: #En caso de no ingresar cualquiera de las opciones disponibles, tiro un error
                print("Opcion invalida!")
                input()

mostrar_menu()