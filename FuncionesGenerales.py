import os
import re
from datetime import date, datetime

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\nPresione Enter para continuar...")

def confirmar_accion(mensaje_pregunta, mensaje_cancelacion="Acción cancelada."):
    """Retorna True si el usuario confirma (s), False si cancela (n)."""
    while True:
        confirmar = input(f"\n{mensaje_pregunta} (s/n) [s]: ").strip().lower() or "s"
        if confirmar == "n":
            print(mensaje_cancelacion)
            pausar()
            limpiar_pantalla()
            return False
        elif confirmar == "s":
            return True
        print("Opción incorrecta.")

def calcular_edad(fecha_tupla):
    """Recibe (Año, Mes, Dia) y retorna edad en años."""
    if not fecha_tupla: return 0
    hoy = date.today()
    año, mes, dia = fecha_tupla
    return hoy.year - año - ((hoy.month, hoy.day) < (mes, dia))

def cargar_dni(persona_tipo="persona"):
    """Pide y valida un DNI."""
    while True:
        dni = input(f"Ingresar DNI del {persona_tipo}: ").strip() 
        if re.match(r"^\d{8}$", dni): # 8 dígitos exactos
            if len(set(dni)) == 1:
                print("DNI inválido (dígitos repetidos).")
                continue
            return int(dni)
        print("DNI inválido. Debe contener 8 dígitos numéricos.")

def cargar_fecha_nacimiento():
    """Pide fecha y retorna tupla (Año, Mes, Dia)."""
    while True:
        fecha_str = input("Ingrese fecha de nacimiento (DD/MM/AAAA): ").strip()
        try:
            fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            if fecha_obj > date.today():
                print("La fecha no puede ser futura.")
                continue
            # Retornamos tupla para mantener compatibilidad con tu lógica
            return (fecha_obj.year, fecha_obj.month, fecha_obj.day)
        except ValueError:
            print("Formato inválido. Use DD/MM/AAAA.")

def cargar_nombre():
    patron = r"^[A-ZÁÉÍÓÚÜÑa-záéíóúüñ\s'-]{2,50}$"
    while True:
        nombre = input("Ingresar Apellido y Nombre: ").strip()
        if re.match(patron, nombre):
            return nombre.title()
        print("Nombre inválido. Use solo letras y espacios.")

def buscar_persona_ui(lista, tipo_busqueda="ambos"):
    """
    Interfaz gráfica para buscar en una lista de diccionarios.
    Retorna el diccionario encontrado o None.
    """
    if not lista:
        print("No hay registros para buscar.")
        pausar()
        return None

    #limpiar_pantalla()
    print("=== BÚSQUEDA ===")
    
    criterio = tipo_busqueda
    if tipo_busqueda == "ambos":
        print("[1] Buscar por DNI")
        print("[2] Buscar por Nombre/Apellido")
        op = input("Ingrese su opción: ").strip()
        criterio = "dni" if op == "1" else "nombre"

    termino = input(f"Ingrese {'DNI' if criterio == 'dni' else 'Nombre'}: ").strip().lower()
    
    resultados = []
    if criterio == "dni":
        resultados = [p for p in lista if termino in str(p.get("DNI", ""))]
    else:
        resultados = [p for p in lista if termino in p.get("Nombre", "").lower()]

    if not resultados:
        print("No se encontraron resultados.")
        pausar()
        return None

    print(f"\n--- Resultados ({len(resultados)}) ---")
    for i, p in enumerate(resultados, 1):
        print(f"[{i}] {p.get('Nombre')} (DNI: {p.get('DNI')})")

    while True:
        try:
            sel = int(input("\nSeleccione # (0 para cancelar): "))
            if sel == 0: return None
            if 1 <= sel <= len(resultados):
                return resultados[sel - 1]
            print("Número fuera de rango.")
        except ValueError:
            print("Ingrese un número válido.")