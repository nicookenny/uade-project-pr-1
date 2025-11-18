import os
import re
from datetime import date

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\nPresione Enter para continuar...")

def confirmar_accion(mensaje_pregunta, mensaje_cancelacion="Acción cancelada por el usuario."):
    while True:
        confirmar = input(f"\n{mensaje_pregunta} (s/n) [s]: ").lower() or "s"
        if confirmar == "n":
            print(mensaje_cancelacion)
            pausar()
            limpiar_pantalla()
            return False
        elif confirmar == "s":
            return True
        print("Opcion incorrecta")
        pausar()

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
            # Rechazar DNIs que tengan los 8 dígitos iguales (00000000, 11111111, ...)
            if len(set(dni)) == 1:
                print("DNI inválido. No se permiten 8 dígitos iguales")
                continue
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
            fecha_obj = date(año, mes, dia)
            hoy = date.today()

            # Permitimos fechas hasta hoy inclusive (recién nacidos y nacidos este año)
            if fecha_obj <= hoy:
                return (año, mes, dia)
            else:
                print("La fecha debe ser anterior o igual a la fecha actual (no puede ser futura)")
        except ValueError:
            print("Fecha inválida. Ingrese números válidos para día, mes y año")

def CargarNombre():
    while True:
        nombre = input("Ingresar el apellido y nombre: ")
        patron_nombre = r"^[A-ZÁÉÍÓÚÜÑa-záéíóúüñ\s'-]{2,50}$"
        if re.match(patron_nombre, nombre):
            return nombre
        print("Nombre no válido. Use solo letras, espacios y caracteres permitidos (-, ')")

def buscar_persona(lista, tipo_busqueda="ambos"):
    """
    Busca personas en una lista por DNI o apellido.
    tipo_busqueda: "ambos" (permite elegir), "dni" o "apellido"
    Retorna: diccionario de la persona seleccionada o None si cancela
    """
    if not lista:
        print("No hay registros para buscar.")
        pausar()
        return None

    limpiar_pantalla()
    print("=" * 50)
    print("BÚSQUEDA DE PERSONA")
    print("=" * 50)

    if tipo_busqueda == "ambos":
        print("\n1. Buscar por DNI")
        print("2. Buscar por Apellido")
        opcion = input("\nElegir opción (1 o 2): ").strip()
        criterio = "dni" if opcion == "1" else "apellido"
    else:
        criterio = tipo_busqueda

    if criterio == "dni":
        termino = input("\nIngrese DNI (números): ").strip()
        resultados = list(filter(lambda p: termino in str(p.get("DNI", "")), lista))
    else:
        termino = input("\nIngrese apellido: ").strip().lower()
        resultados = list(filter(lambda p: termino in p.get("Nombre", "").lower(), lista))

    if not resultados:
        print("\nNo se encontraron resultados.")
        pausar()
        return None

    limpiar_pantalla()
    print("=" * 50)
    print("RESULTADOS DE BÚSQUEDA")
    print("=" * 50)

    for i, persona in enumerate(resultados, 1):
        print(f"\n{i}. DNI: {persona['DNI']} | {persona['Nombre']}")

    while True:
        try:
            seleccion = int(input("\nSeleccionar persona (número): ")) - 1
            if 0 <= seleccion < len(resultados):
                return resultados[seleccion]
            print("Selección inválida.")
        except ValueError:
            print("Ingrese un número válido.")

def registrarErrores(error):
    try:
        archivo = open("C:\\Users\\Jesus\\Desktop\\JAVA--PROGRA2\\uade-project-pr-1\\Errores.txt" ,mode = "a" ,encoding="utf-8")
        try:
            error = f"Tipo:{type(error)} - Mensaje: {str(error)}\n"
            print(f"Ocurrio un error: {error}")
            archivo.write(error)
        finally:
            archivo.close()
    except Exception as logError:
        print(f"Error al escribir en el log: {logError}")
