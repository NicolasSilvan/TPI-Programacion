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

def menor_poblacion(stock):
    guardado=None
    for pais in stock:
        poblacion=pais["poblacion"]
        if guardado is None or poblacion < guardado:
            guardado=pais["poblacion"]
            guardado2=pais["nombre"]
    return guardado2, guardado

def mayor_poblacion(stock):
    guardado=None
    for pais in stock:
        poblacion=pais["poblacion"]
        if guardado is None or poblacion > guardado:
            guardado=pais["poblacion"]
            guardado2=pais["nombre"]
    return guardado2, guardado

def promedio_poblacion(stock):
    suma=0
    for pais in stock:
        poblacion=pais["poblacion"]
        suma+=poblacion
    return suma/len(stock)      

def promedio_superficie(stock):
    suma=0
    for pais in stock:
        superficie=pais["superficie"]
        suma+=superficie
    return suma/len(stock) 

def cantidad_paises(stock, continente):
    cantidad=0
    for pais in stock:
        if pais["continente"] == continente:
            cantidad+=1
    return cantidad

def mostrar_estadisticas():
    print("=== Estadisticas ===")
    stock = obtener_paises() #llamo a la funcion que carga la info en el archivo
    while True:
        print("== Opciones ==")
        print("1) Pais con mayor y menor población")
        print("2) Promedio de población")
        print("3) Promedio de superficie")
        print("4) Cantidad de paises por continente")
        print("5) Salir")
        eleccion=int(input("¿Que opcion desea? "))
        match eleccion:
            case 1:
                pais1, poblacion1 = mayor_poblacion(stock)
                pais2, poblacion2 = menor_poblacion(stock)
                print(f"El pais con mayor poblacion es {pais1} con {poblacion1} habitantes.")
                print(f"El pais con menor poblacion es {pais2} con {poblacion2} habitantes.")
                input()
            case 2:
                promedio=promedio_poblacion(stock)
                print(f"El promedio de población es {promedio} habitantes.")
                input()
            case 3:
                promedio=promedio_superficie(stock)
                print(f"El promedio de superficie es {promedio} km2.")
                input()
            case 4:
                continente=input("Ingrese el continente: ")
                if validar_continente(continente):
                    cantidad=cantidad_paises(stock, continente)
                    print(f"Hay {cantidad} paises en {continente}.")
                else:
                    print("Continente no encontrado en los datos.")
                input()
            case 5:
                print("Saliendo...")
                input()
                break
            case _:
                print("Opcion invalida!.")
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
    if os.path.getsize(NOMBRE_ARCHIVO) == 0: #si el archivo esta vacio, agrego la informacion con los headers
        with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"])
            escritor.writeheader()
            escritor.writerow(pais)

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
        print(f"== Poblacion : {poblacion}")
        print(f"== Superficie : {superficie}")
        print(f"== Continente : {continente}")
        input()
    
def guardar_paises(paises): #sobreescribo la informacion del archivo, y creo los headers de nuevo
    with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"])
        escritor.writeheader()
        escritor.writerows(paises)

def actualizar_poblacion_superficie():
    print("=== Actualizar Poblacion Y Superficie ===")
    pais_nombre = input("Ingrese el nombre del pais a actualizar: ")

    encontrado = True #agrego esta variable para verificar que se encontro el pais en el archivo

    if not pais_nombre: #valido que el pais no este vacio
        print("El pais no puede estar vacio!")
        input()
        return
    
    paises = obtener_paises()

    if not paises: #valido que el archivo no este vacio
        print("El archivo no contiene ningun pais.")
        input()
        return

    for pais in paises:
        if pais["nombre"].lower() == pais_nombre.lower(): #busco que exista el pais adentro del archivo

            encontrado = True

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

                    guardar_paises(paises)
                    print("La poblacion fue actualizada!")
                    input()
                case "s": #superficie
                    superficie = input("Ingrese el numero de superficie en KM2 a actualizar: ")

                    if not validar_poblacion_superficie(superficie): #valido que la superficie no sea 0 o negativo
                        print("La superficie no es valida!")
                        input()
                        return
                    
                    pais["superficie"] = int(superficie) #le asigno el nuevo numero de superficie al archivo
                
                    guardar_paises(paises)
                    print("La superficie fue actualizada!")
                    input()
                case _:
                    print("Opcion invalida!")
                    input()
                    return
            
            break
        else:
            encontrado = False

    if not encontrado:
        print(f"El pais {pais_nombre} no se encuentra en el archivo!")
        input()
        return

def buscar_pais():
    print("=== BUSCAR PAISES ===")
    pais_busqueda = input("Ingrese el nombre del pais que busca: ").strip().lower()

    if not pais_busqueda: #valido que el pais no este vacio
        print("El pais no puede estar vacio!")
        input()
        return
    
    if not existe_pais(pais_busqueda): #valido que el pais exista en el archivo
        print("Ese pais no se encuentra en los datos o no existe.")
        input()
        return

    paises = obtener_paises()

    for pais in paises: #recorro el archivo en busqueda de la info del pais a buscar
        if pais["nombre"].lower() == pais_busqueda:
            print(f"Nombre : {pais["nombre"]} \nPoblación : {pais["poblacion"]} \nSuperficie : {pais["superficie"]} \nContinente : {pais["continente"]}")
            input()
            break

def filtrar_paises():
    print("=== FILTRAR PAISES ===")
    filtro = input("Desea filtrar el filtro por:\n(C) Continente\n(P) Rango de Poblacion\n(S) Rango de Superficie\n(C/P/S):").strip()

    paises = obtener_paises() #voy a buscar los paises por fuera del match asi los puedo usar en todos los case

    match filtro.lower(): #hago un match case para cada filtro
        case "c":
            print("=== FILTRO CONTINENTE ===")
            continente = input("Ingrese el continente a filtrar: ").strip()

            if not validar_continente(continente.lower()): #valido que el continente sea valido y exista
                print("El continente ingresado no existe o esta vacio! Debe ingresar un continente valido.")
                input()
                return
            
            paises_filtrados = [p for p in paises if p["continente"].lower() == continente.lower()] #filtro usando list comprehension
            
            if not paises_filtrados: #si el filtro queda vacio es por que no hay ninguno en el archivo
                print(f"No se encontro ningun pais en el archivo que pertenezca al continente {continente}!")
                input()
                return
            
            print("=======================================")
            print(f"Paises del continente {continente}:")
            print("=======================================")
        case "p":
            print("=== FILTRO RANGO DE POBLACION ===")
            poblacion_desde = input("Filtrar rango de poblacion DESDE: ")

            if not validar_poblacion_superficie(poblacion_desde): #reviso que sea un valor valido y no >= 0
                print("El numero de poblacion no es valido! Debe ingresar un valor mayor que 0.")
                input()
                return
            
            poblacion_hasta = input("Filtrar rango de poblacion HASTA: ") #reviso que sea un valor valido y no >= 0

            if not validar_poblacion_superficie(poblacion_hasta):
                print("El numero de poblacion no es valido! Debe ingresar un valor mayor que 0.")
                input()
                return

            poblacion_desde = int(poblacion_desde)
            poblacion_hasta = int(poblacion_hasta)

            if poblacion_desde > poblacion_hasta: #valido que el rango desde no sea mayor que el hasta
                print("El rango DESDE no puede ser mayor al rango HASTA!")
                input()
                return
            
            paises_filtrados = [p for p in paises if p["poblacion"] >= poblacion_desde and p["poblacion"] <= poblacion_hasta] #filtro usando list comprehension

            if not paises_filtrados: #si el filtro queda vacio es por que no hay ninguno en el archivo
                print(f"No se encontro ningun pais en el archivo que este en ese rango de poblacion!")
                input()
                return
            
            print("======================================")
            print(f"Paises dentro del rango de poblacion:")
            print("=======================================")
        case "s":
            print("=== FILTRO RANGO DE SUPERFICIE ===")

            superficie_desde = input("Filtrar rango de Superficie DESDE: ")

            if not validar_poblacion_superficie(superficie_desde): #reviso que sea un valor valido y no >= 0
                print("El numero de superficie no es valido! Debe ingresar un valor mayor que 0.")
                input()
                return
            
            superficie_hasta = input("Filtrar rango de superficie HASTA: ") #reviso que sea un valor valido y no >= 0

            if not validar_poblacion_superficie(superficie_hasta):
                print("El numero de superficie no es valido! Debe ingresar un valor mayor que 0.")
                input()
                return

            superficie_desde = int(superficie_desde)
            superficie_hasta = int(superficie_hasta)

            if superficie_desde > superficie_hasta: #valido que el rango desde no sea mayor que el hasta
                print("El rango DESDE no puede ser mayor al rango HASTA!")
                input()
                return
            
            paises_filtrados = [p for p in paises if p["superficie"] >= superficie_desde and p["superficie"] <= superficie_hasta] #filtro usando list comprehension

            if not paises_filtrados: #si el filtro queda vacio es por que no hay ninguno en el archivo
                print(f"No se encontro ningun pais en el archivo que este en ese rango de superficie!")
                input()
                return
            
            print("=======================================")
            print(f"Paises dentro del rango de superficie:")
            print("=======================================")
        case _:
            print("Opcion invalida!")
            input()
            return

    for pais in paises_filtrados: #hago el for de los paises filtrados afuera para no repetirlo por cada filtro
        print(f"Pais = {pais["nombre"]} - Poblacion = {pais["poblacion"]} - Superficie = {pais["superficie"]} - Continente = {pais["continente"]}")
    
    input()

def ordenar_paises():
    print("=== ORDENAR PAISES ===")

    orden = input("Desea ordenar los pasies por\n(N) Nombre\n(P) Poblacion\n(S) Superficie(Ascendente/Descendente)\n(N/P/S):").strip()

    paises = obtener_paises() #voy a buscar los paises por fuera del match asi los puedo usar en todos los case

    match orden.lower():
        case "n":
            paises_ordenados = sorted(paises, key=lambda p: p["nombre"].lower()) #ordeno la lista por el campo 'nombre'

            print("=== Paises ordenados por orden alfabetico ===")
        case "p":
            asc_desc = input("Desea ordenar la poblacion de manera ASCENDENTE(A) o DESCENDENTE(D): (A/D)").strip()

            match asc_desc.lower():
                case "a":
                    paises_ordenados = sorted(paises, key=lambda p: p["poblacion"])

                    print("=== Paises ordenados por poblacion ascendente ===")
                case "d":
                    paises_ordenados = sorted(paises, key=lambda p: p["poblacion"], reverse=True)

                    print("=== Paises ordenados por poblacion descendente ===")
                case _:
                    print("Opcion invalida!")
                    input()
                    return
        case "s":
            asc_desc = input("Desea ordenar la superficie de manera ASCENDENTE(A) o DESCENDENTE(D): (A/D)").strip()

            match asc_desc.lower():
                case "a":
                    pass
                case "d":
                    pass
                case _:
                    print("Opcion invalida!")
                    input()
                    return
        case _:
            print("Opcion invalida!")
            input()
            return

    for pais in paises_ordenados:    
        print(f"Pais = {pais["nombre"]} - Poblacion = {pais["poblacion"]} - Superficie = {pais["superficie"]} - Continente = {pais["continente"]}")
    input()

def mostrar_menu():
    opcion = ""
    while opcion != 7: #mientras la opcion no sea 7 el programa va a seguir ejecutandose
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
                buscar_pais()
            case "4":
                filtrar_paises()
            case "5":
                ordenar_paises()
            case "6":
                mostrar_estadisticas()
            case "7":
                print("Gracias por usar nuestro programa!")
                input()
                break
            case _: #En caso de no ingresar cualquiera de las opciones disponibles, tiro un error
                print("Opcion invalida!")
                input()

mostrar_menu()