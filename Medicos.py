import os
import Datos
#from Datos import medicos ---------Cambie este porque usamos muchos datos dentro de este codigo-------- 
from datetime import date

def CalculoEdad(fecha):
    hoy = date.today()
    año, mes, dia = fecha
    edad = hoy.year - año - ((hoy.month, hoy.day) < (mes, dia))
    return edad

def MostrartablaMedicos():
  os.system('cls')
  print(f"{'ID':<3} {'Nombre':<20} {'Edad':<12} {'DNI':<10} {'Especialidad':<30} {'Estado':<12} {'Paciente'}")
  print("-"*102)
  for medico in Datos.medicos: # Cada vez que quieras llamar a un diccionario o una tupla le Agregas Datos.Nombre de la tupla o diccionario A usar 
      for id_medico, datos in medico.items():
        print(f"{id_medico:<3} {datos['Nombre']:<20} {CalculoEdad(datos['Fecha de Nacimiento']):<12} {datos['DNI']:<10} {datos['Especialidad']:<30} {datos['Estado']:<12} {datos['Paciente']}")
  input("\nPresione Enter para continuar...")

def CargaEspecialidad():
    print("="*40)
    for areas in Datos.especialidades_medicas:
        print(areas)
    print("="*40)
    especialidad=input("Ingresar la especialidad:")
    while especialidad not in Datos.especialidades_medicas:
        print("Especialidad no encontrada")
        especialidad = input("Ingresar otra especialidad: ")
    return especialidad

def CargarFechaDeNacimiento():
    carga = True
    while carga:
        dia = int(input("Ingrese su dia de nacimiento: "))
        mes = int(input("Ingrese su mes de nacimiento: "))
        año = int(input("Ingrese su año de nacimiento: "))
        fecha = (año, mes, dia)
        edad = CalculoEdad(fecha)
        if 24 <= edad <= 70:
            carga = False
        else:
            print("Fecha invalida")
    return fecha

def CargarDNI():
    dni = input("Ingresar número de documento: ")
    while not dni.isdigit() or len(dni) != 8:
        print("DNI inválido")
        dni = input("Ingresar otro número de documento: ")
    return int(dni)

def CargarNombre():
    nombre= input("Ingresar el nombre: ")
    while nombre == "" or nombre.isnumeric():
        print("Nombre no válido")
        nombre = input("Ingrese otro nombre: ")
    return nombre

def CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad):
    medico = {len(Datos.medicos) + 1: {
        "Nombre": nombre,
        "Fecha de Nacimiento": FechaDeNacimiento,
        "DNI": dni,
        "Especialidad": Especialidad,
        "Estado": "Disponible",
        "Paciente": "Ninguno"
    }}
    return medico

def agregarMedico(): #Agrega un medico al diccionario
    os.system('cls')
    while True:
        band = True
        print("="*40)
        MostrartablaMedicos()
        dni = CargarDNI()

        # Buscar si el médico ya existe
        for diccionario in Datos.medicos:
            for medico, datos in diccionario.items():
                if dni == datos["DNI"]:
                    print(f"El médico {datos['Nombre']} ya existe")
                    band = False
                    break

        if band: # Solo se agrega si no existe
            nombre = CargarNombre()
            FechaDeNacimiento = CargarFechaDeNacimiento()
            Especialidad = CargaEspecialidad()
            Datos.medicos.append(CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad)) # Manera de guardar las modificaciones en el archivo de datos
            print("El medico se agregó correctamente")
            input("\nPresione Enter para continuar...")
            break
        else: 
            input("\nPresione Enter para continuar")
            os.system('cls')
    
    MostrartablaMedicos()
    os.system('cls')

def eliminarMedico():#Elimina de la lista al medico
    os.system('cls')
    MostrartablaMedicos()
    while True:
        band = True
        print()
        print("="*40)
        dni = int(input("Ingresar numero de documento: "))#Se busca si el medico existe a traves de su DNI a traves un True/False
        for diccionario in Datos.medicos:
            for medico,datos in diccionario.items():
                #print(datos["Paciente"])
                if dni == datos["DNI"] and datos["Paciente"] == 'Ninguno':
                    band = False
        
        if band == False:#Iteramos para buscar el indice(posicion) del medico para poder eliminarlo de la lista y forzamos que el bucle rompa a traves de un return con el fin de no tener IndexError
            for diccionario in range(len(Datos.medicos)):
                for medico,datos in Datos.medicos[diccionario].items():
                    if dni == datos["DNI"]:
                        #print(medico)
                        del Datos.medicos[diccionario][medico]
                        print(f'El medico {datos["Nombre"]} se elimino correctamente de la lista')
                        input("\nPresione Enter para continuar...")
                        return
                    
        else:
            print("El medico no esta en la lista o tiene informacion importante")
            input("\n presione enter para continuar")
            os.system('cls')
    

def modificarMedico():#Modifica datos del medico
    os.system('cls')
    while True:    
        encontrado = False
        MostrartablaMedicos()
        dni = CargarDNI()
        for diccionario in Datos.medicos:
            for medico,datos in diccionario.items():
                if dni == datos["DNI"] and datos["Paciente"] == 'Ninguno':
                    encontrado = True
                    #Modificar los datos
                    FechaDeNacimiento = CargarFechaDeNacimiento()
                    nombre = CargarNombre()
                    especialidad = CargaEspecialidad()
                    
                    datos["Nombre"] = nombre
                    datos["Fecha de Nacimiento"] = FechaDeNacimiento
                    datos["Especialidad"] = especialidad
                    
                    print("Se han modificado sus datos correctamente \n")
                    MostrartablaMedicos()
                    os.system('cls')
                    return
        
        if not encontrado:
            print("El medico no está en la lista o tiene información importante")
            input("\nPresione Enter para continuar")
            os.system('cls')

"""
Esta funcion se encarga de mostrar el historial de los pacientes que se atendieron con un medico, ademas de comparar entre dos medicos sus historiales
"""

def mostrarHistorialMedico():
    os.system('cls')
    while True:
        print("\n" + "="*40)
        print("[1] , Mostrar historial de un medico" )
        print("[2] , Mostrar historial entre 2 Medicos " )
        opcion = int(input("Ingresar una Opcion: "))#Podes elegir comparar historiales o ver uno solo
        if opcion == 1:
            while True:
                MostrartablaMedicos()
                dni = int(input("Ingresar numero de documento del Medico: "))#Verificamos que el medico existe
                for diccionario in Datos.medicos:
                    for medico,dato in diccionario.items():
                        print(dato["DNI"])
                        if dni == dato["DNI"]:
                            while True:
                                if len(dato["Historial"]) < 3 and len(dato["Historial"]) >= 1:#Si el historial es menor que 3 pacientes lo muestra en pantalla con un print
                                    print(f'{dato["Historial"]}')
                                    input("\nPresione Enter para continuar")
                                    return
                                elif dato["Historial"] == []:#Si el historial es una lista vacia que 3 quiere decir que el medico no atendio a ningun paciente
                                    print("El medico no tiene historial clinico")
                                    input("\nPresione Enter para continuar")
                                    os.system('cls')
                                    return
                                else:
                                    print("\n" + "="*40)
                                    print("[1] , Mostrar los primeros 6 pacientes" )
                                    print("[2] , Mostrar todo el historial Medico " )
                                    opcio = int(input("Ingresar una Opcion: "))
                                    if opcio == 1:
                                        ultimosTres = dato['Historial'][:6] # a traves de la tecnica de rebanado mostramos hasta los primeros 6 pacientes 
                                        print(f'{ultimosTres}')
                                        input("\nPresione Enter para continuar")
                                        os.system('cls')
                                        return
                                    elif opcio== 2:# Muestra el historial completo de los pacientes atendidos por el medico
                                        print(f'{dato["Historial"]}')
                                        input("\nPresione Enter para continuar")
                                        os.system('cls')
                                        return
                                    else:
                                        print("Opcion incorrecta")
                                        input("\nPresione Enter para continuar")
                                        os.system('cls')

                print("El medico no esta en la lista")
                input("\nPresione Enter para continuar")
                os.system('cls')

        if opcion == 2:#Compara entre dos medicos sus historiales
            os.system('cls')
            MostrartablaMedicos()
            while True:
                band = False
                medico1 = int(input("Ingresar numero de documento del primer medico elegido: "))#Verificamos que exista el primer medico
                for diccionario in Datos.medicos:
                    for medico,datos in diccionario.items():
                        if medico1 == datos['DNI'] and datos['Historial'] != []:
                            auxMedico1 = datos
                            id1 = medico
                            band = True
                if band == True:
                    while True:
                        band1 = False
                        medico2 = int(input("Ingresar numero de documento del segundo medico elegido: "))#Verificamos que exista el segundo medico
                        for diccionario in Datos.medicos:
                            for medic,dato in diccionario.items():
                                if medico2 == dato['DNI'] and dato['Historial'] != [] and dato['DNI']:
                                    auxMedico2 = dato
                                    id2 = medic
                                    band1 = True
                        
                        if band1 == True:
                            if auxMedico1 == auxMedico2: #Verificamos que no sea el mismo medico el que se compara
                                print("Los medicos son los mismos, eliga otro por favor")
                                input("\nPresione Enter para continuar")
                            else:
                                os.system('cls')
                                historial1_dict = {}
                                historial2_dict = {}
                                for medico in Datos.medicos: #Iteramos por la clave del medico y su valor del historial para agregarlo a un diccionario
                                    if id1 in medico:
                                        for paciente in medico[id1]["Historial"]:
                                            historial1_dict.update(paciente)
                                    if id2 in medico:
                                        for paciente in medico[id2]["Historial"]:
                                            historial2_dict.update(paciente)
                                print(historial1_dict)
                                
                                """
                                Convertimos a cada diccionario en un conjunto para utilizar operaciones con el fin de comparar cada historial
                                """
                                historialMedico1 = set(historial1_dict.keys()) 
                                historialMedico2 = set(historial2_dict.keys())

                                comunes = historialMedico1 & historialMedico2
                                exclusivosPrimero = historialMedico1 - historialMedico2
                                exclusivosSegundo = historialMedico2 - historialMedico1

                                print("\nPacientes en comun:")
                                for pacientes in comunes:
                                    print(historial1_dict[pacientes])

                                print("\nPacientes exclusivos del primero:")
                                for pacientes in exclusivosPrimero:
                                    print(historial1_dict[pacientes])

                                print("\nPacientes exclusivos del segundo:")
                                for pacientes in exclusivosSegundo:
                                    print(historial2_dict[pacientes])

                                input("\nPresione Enter para continuar")
                                os.system('cls')
                                return
                                
                        else:            
                            print("El medico no esta en la lista o el historial medico esta vacio")
                            input("\nPresione Enter para continuar")
                            os.system('cls')
                else:

                    print("El medico no esta en la lista o el historial medico esta vacio")
                    input("\nPresione Enter para continuar")
                os.system('cls')
def main():
    ...
main()