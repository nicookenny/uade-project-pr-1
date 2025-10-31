import os
import re
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

def CargarDNI(persona):
    while True:
        dni = input(f"Ingresar número de documento del {persona}: ")
        patron_dni = r"^\d{8}$"
        if re.match(patron_dni, dni):
            return int(dni)
        print("DNI inválido. Debe contener exactamente 8 dígitos numéricos.")

def CargarFechaDeNacimiento():
    while True:
        try:
            patron_fecha = r"^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/\d{4}$"
            fecha_str = input("Ingrese su fecha de nacimiento (DD/MM/AAAA): ")
            
            if not re.match(patron_fecha, fecha_str):
                print("Formato de fecha inválido. Use DD/MM/AAAA")
                continue
                
            dia, mes, año = map(int, fecha_str.split('/'))
            fecha = (año, mes, dia)
            edad = CalculoEdad(fecha)
            
            if edad > 0:
                return fecha
            print("La fecha debe ser anterior a la fecha actual")
        except ValueError:
            print("Fecha inválida. Ingrese números válidos para día, mes y año")

def CargarNombre():
    while True:
        nombre = input("Ingresar el apellido y nombre: ")
        patron_nombre = r"^[A-ZÁÉÍÓÚÜÑa-záéíóúüñ\s'-]{2,50}$"
        if re.match(patron_nombre, nombre):
            return nombre
        print("Nombre no válido. Use solo letras, espacios y caracteres permitidos (-, ')")