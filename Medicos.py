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
                    
                    print("Se han modificado sus datos correctamente")
                    input("\nPresione Enter para continuar")
                    return
        
        if not encontrado:
            print("El medico no está en la lista o tiene información importante")
            input("\nPresione Enter para continuar")
            os.system('cls')

def main():
    ...
main()