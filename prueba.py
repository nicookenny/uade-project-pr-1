import os
#from datetime import date
#from Datos import medicos
import Medicos
import Datos

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
        edad = Medicos.CalculoEdad(fecha)
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
    while True:
        band = True
        print("="*40)
        Medicos.MostrartablaMedicos()
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
            Datos.medicos.append(CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad))
            print("El medico se agregó correctamente")
            input("\nPresione Enter para continuar...")
            break
        else: 
            input("\nPresione Enter para continuar")
            os.system('cls')
    
    Medicos.MostrartablaMedicos()

agregarMedico()
