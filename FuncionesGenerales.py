import os
from datetime import date

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\nPresione Enter para continuar...")

def CalculoEdad(fecha):
    """
    Calcula la edad de una persona a partir de su fecha de nacimiento.
    """
    hoy = date.today()
    año, mes, dia = fecha
    edad = hoy.year - año - ((hoy.month, hoy.day) < (mes, dia))
    return edad

def CargarDNI():
    dni = input("Ingresar número de documento: ")
    while not dni.isdigit() or len(dni) != 8:
        print("DNI inválido")
        dni = input("Ingresar otro número de documento: ")
    return int(dni)

def CargarFechaDeNacimiento():
    carga = True
    while carga:
        dia = int(input("Ingrese su dia de nacimiento: "))
        mes = int(input("Ingrese su mes de nacimiento: "))
        año = int(input("Ingrese su año de nacimiento: "))
        fecha = (año, mes, dia)
        edad = CalculoEdad(fecha)
        if edad > 0:
            carga = False
        else:
            print("Fecha invalida")
    return fecha

def CargarNombre():
    nombre = input("Ingresar el apellido y nombre: ")
    while nombre == "" or nombre.isnumeric():
        print("Nombre no válido")
        nombre = input("Ingrese otro apellido y nombre: ")
    return nombre