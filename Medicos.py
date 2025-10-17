import FuncionesGenerales
import Datos
from functools import reduce
from datetime import date


#Funciones para visualizar datos
def mostrar_historial(historial):
    for paciente in historial:
        print(f"DNI: {paciente['DNI']}")
        print(f"  Nombre: {paciente['Nombre']}")
        print(f"  Fecha de Nacimiento: {paciente['Fecha de Nacimiento'][2]:02d}/{paciente['Fecha de Nacimiento'][1]:02d}/{paciente['Fecha de Nacimiento'][0]}")
        print(f"  Obra Social: {paciente['Obra Social']}")
        print(f"  Fecha Turno: {paciente['Fecha Turno'][2]:02d}/{paciente['Fecha Turno'][1]:02d}/{paciente['Fecha Turno'][0]}")
        print("-" * 30)

def mostrar_historial_paginado(historial, cantidad=6):
    total = len(historial)
    inicio = 0
    while inicio < total:
        print("-" * 30)
        fin = min(inicio + cantidad, total)
        for paciente in historial[inicio:fin]:
            print(f"DNI: {paciente['DNI']}")
            print(f"  Nombre: {paciente['Nombre']}")
            print(f"  Fecha de Nacimiento: {paciente['Fecha de Nacimiento'][2]:02d}/{paciente['Fecha de Nacimiento'][1]:02d}/{paciente['Fecha de Nacimiento'][0]}")
            print(f"  Obra Social: {paciente['Obra Social']}")
            print(f"  Fecha Turno: {paciente['Fecha Turno'][2]:02d}/{paciente['Fecha Turno'][1]:02d}/{paciente['Fecha Turno'][0]}")
            print("-" * 30)
        inicio += cantidad
        if inicio < total:
            respuesta = input("¿Desea ver más historiales? (s/n): ").lower()
            if respuesta != "s":
                break

def visualizarDatos(lista,Encabezado):
    FuncionesGenerales.limpiar_pantalla()
    print("=" * 40)
    print(f"{Encabezado}")
    print(f"Nombre completo: {lista['Nombre']}")
    print(f"Fecha de Nacimiento: {lista['Fecha de Nacimiento'][2]}/{lista['Fecha de Nacimiento'][1]}/{lista['Fecha de Nacimiento'][0]}")
    print(f"Edad:{FuncionesGenerales.CalculoEdad(lista['Fecha de Nacimiento'])} años")
    print(f"DNI: {lista['DNI']}")
    print(f"Especialidad: {lista['Especialidad']}")
    if "Horarios" in lista:
        print("Horarios de atención:")
        for dia, horario in lista["Horarios"].items():
            if horario:
                print(f"  {dia}: {horario[0]}:00 - {horario[1]}:00")
            else:
                print(f"  {dia}: No disponible")
    else:
        print(f"Estado: {lista['Estado']}")
    print("=" * 40)

def MostrartablaMedicos():
    FuncionesGenerales.limpiar_pantalla()
    print(
        f"{'ID':<3} {'Nombre':<20} {'Edad':<12} {'DNI':<10} {'Especialidad':<30} {'Turnos Hoy':<12}"
    )
    print("-" * 90)
    for i, medico in enumerate(Datos.medicos, 1):
        hoy = date.today()
        fecha_hoy = (hoy.year, hoy.month, hoy.day)
        turnos_hoy = len([t for t in Datos.turnos if t["medico_dni"] == medico["DNI"] and t["fecha"] == fecha_hoy and t["estado"] == "Confirmado"])
        print(
            f"{i:<3} {medico['Nombre']:<20} {FuncionesGenerales.CalculoEdad(medico['Fecha de Nacimiento']):<12} {medico['DNI']:<10} {medico['Especialidad']:<30} {turnos_hoy:<12}"
        )
    FuncionesGenerales.pausar()

#Funciones de busqueda

def buscar_medico_por_dni(dni):
    existentes = [medico["DNI"] for medico in Datos.medicos]

    if dni in existentes:
        medico = reduce(lambda x, y: y if y["DNI"] == dni else x, Datos.medicos, None)
        return medico
    return None

def medico_existe(dni):
    existentes = [medico["DNI"] for medico in Datos.medicos]
    if dni in existentes:
        return True
    return False

#Funciones de carga de datos

def CargaEspecialidad():
    print("=" * 40)
    for areas in Datos.especialidades_medicas:
        print(areas)
    print("=" * 40)
    especialidad = input("Ingresar la especialidad: ")
    while especialidad not in Datos.especialidades_medicas:
        print("Especialidad no encontrada")
        especialidad = input("Ingresar otra especialidad: ")
    return especialidad

def CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad):
    return {
        "Nombre": nombre,
        "Fecha de Nacimiento": FechaDeNacimiento,
        "DNI": dni,
        "Especialidad": Especialidad,
        "Estado": "Disponible",
        "Paciente": {},
        "Horarios": {
            "Lunes": (9, 18),
            "Martes": (9, 18),
            "Miércoles": (9, 18),
            "Jueves": (9, 18),
            "Viernes": (9, 18),
            "Sábado": None,
            "Domingo": None
        },
        "Historial": [],
    }

def medico_disponible(datos_medico):
    return datos_medico["Paciente"] == {}

"""
Opción 2 (menu)
"""

def agregarMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        print("=" * 40)
        MostrartablaMedicos()
        dni = FuncionesGenerales.CargarDNI()

        existe = medico_existe(dni)

        if existe:
            medicoExistente = buscar_medico_por_dni(dni)
            print(f"El médico {medicoExistente['Nombre']} ya existe")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
        else:
            nombre = FuncionesGenerales.CargarNombre()
            FechaDeNacimiento = FuncionesGenerales.CargarFechaDeNacimiento()
            Especialidad = CargaEspecialidad()
            newMedico=CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad)
            visualizarDatos(newMedico,Encabezado="Resumen de datos del nuevo médico:")
            confirmar = input("\n¿Desea confirmar el alta del médico? (s/n): ").lower()
            if confirmar != "s":
                print("Alta cancelada por el usuario.")
                FuncionesGenerales.pausar()
                FuncionesGenerales.limpiar_pantalla()
                return

            Datos.medicos.append(newMedico)
            print(f"El medico {nombre} se agregó correctamente")
            FuncionesGenerales.pausar()
            break

    MostrartablaMedicos()
    FuncionesGenerales.limpiar_pantalla()

"""
Opción 3 (menu)
"""
def eliminarMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        MostrartablaMedicos()
        print()
        print("=" * 40)
        dni = FuncionesGenerales.CargarDNI()

        existe = medico_existe(dni)
        if not existe:
            print("El medico no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        medicoExistente = buscar_medico_por_dni(dni)
        if not medico_disponible(medicoExistente):
            print("El medico tiene informacion importante y no puede ser eliminado")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        nombre_medico = medicoExistente["Nombre"]
        visualizarDatos(medicoExistente,Encabezado="Datos del medico a eliminar:")
        confirmar = input("\n¿Desea confirmar? (s/n): ").lower()
        if confirmar != "s":
            print("Modificación cancelada por el usuario.")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return
        index = Datos.medicos.index(medicoExistente)
        del Datos.medicos[index]
        print(f"El medico {nombre_medico} se elimino correctamente de la lista")
        FuncionesGenerales.pausar()
        MostrartablaMedicos()
        return

"""
Opción 4 (menu)
"""

def modificarMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        MostrartablaMedicos()
        dni = FuncionesGenerales.CargarDNI()

        existe = medico_existe(dni)
        if not existe:
            print("El medico no está en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        medicoExistente = buscar_medico_por_dni(dni)
        if not medico_disponible(medicoExistente):
            print("El medico tiene información importante y no puede ser modificado")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        FechaDeNacimiento = FuncionesGenerales.CargarFechaDeNacimiento()
        nombre = FuncionesGenerales.CargarNombre()
        especialidad = CargaEspecialidad()

        medicoExistente["Nombre"] = nombre
        medicoExistente["Fecha de Nacimiento"] = FechaDeNacimiento
        medicoExistente["Especialidad"] = especialidad
        visualizarDatos(medicoExistente,Encabezado="Datos del medico modificados:")
        confirmar = input("\n¿Desea confirmar? (s/n): ").lower()
        if confirmar != "s":
            print("Modificación cancelada por el usuario.")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return

        print("Se han modificado sus datos correctamente\n")
        MostrartablaMedicos()
        FuncionesGenerales.limpiar_pantalla()
        return

"""
Opción 5 (menu)
"""

def mostrarHistorialMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        print("\n" + "=" * 40)
        print("[1] Mostrar historial de un medico")
        print("[2] Mostrar historial entre 2 Medicos")
        opcion = int(input("Ingresar una Opcion: "))
        if opcion == 1:
            mostrarHistorialMedico1()
            return
        elif opcion == 2:
            mostrarHistorialMedico2()
            return
        else:
            print("Opción inválida")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()


def mostrar_opciones_historial(historial):
    if not historial:
        print("El medico no tiene historial clinico")
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return True

    if len(historial) < 3:
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return True

    print("\n" + "=" * 40)
    print("[1] Mostrar los primeros 6 pacientes")
    print("[2] Mostrar todo el historial Medico")
    opcion = int(input("Ingresar una Opcion: "))

    if opcion == 1:
        mostrar_historial_paginado(historial)
    elif opcion == 2:
        mostrar_historial(historial)
    else:
        print("Opcion incorrecta")

    FuncionesGenerales.pausar()
    FuncionesGenerales.limpiar_pantalla()
    return True


def mostrarHistorialMedico1():
    while True:
        MostrartablaMedicos()
        dni = int(input("Ingresar numero de documento del Medico: "))

        existe = medico_existe(dni)
        if not existe:
            print("El medico no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        medicoExistente = buscar_medico_por_dni(dni)
        if mostrar_opciones_historial(medicoExistente["Historial"]):
            return


def obtener_historial_dict(dni_medico):
    historial_dict = {}
    medico = buscar_medico_por_dni(dni_medico)
    if medico:
        for paciente in medico["Historial"]:
            historial_dict[paciente["DNI"]] = paciente
    return historial_dict


def mostrarHistorialMedico2():
    FuncionesGenerales.limpiar_pantalla()
    MostrartablaMedicos()

    medico1_dni = int(input("Ingresar numero de documento del primer medico elegido: "))

    medico1Existe = medico_existe(medico1_dni)
    if not medico1Existe:
        print("El primer medico no esta en la lista o su historial esta vacio")
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return

    medico2_dni = int(
        input("Ingresar numero de documento del segundo medico elegido: ")
    )

    medico2Existe = medico_existe(medico2_dni)

    if not medico2Existe:
        print("El segundo medico no esta en la lista o su historial esta vacio")
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return

    if medico1_dni == medico2_dni:
        print("Los medicos son los mismos, eliga otro por favor")
        FuncionesGenerales.pausar()
        return

    FuncionesGenerales.limpiar_pantalla()
    historial1_dict = obtener_historial_dict(medico1_dni)
    historial2_dict = obtener_historial_dict(medico2_dni)

    historialMedico1 = set(historial1_dict.keys())
    historialMedico2 = set(historial2_dict.keys())

    comunes = historialMedico1 & historialMedico2
    exclusivosPrimero = historialMedico1 - historialMedico2
    exclusivosSegundo = historialMedico2 - historialMedico1

    print("\nPacientes en comun:")
    for dni_paciente in comunes:
        paciente = historial1_dict[dni_paciente]
        print(f"  {paciente['Nombre']} (DNI: {paciente['DNI']})")

    print("\nPacientes exclusivos del primero:")
    for dni_paciente in exclusivosPrimero:
        paciente = historial1_dict[dni_paciente]
        print(f"  {paciente['Nombre']} (DNI: {paciente['DNI']})")

    print("\nPacientes exclusivos del segundo:")
    for dni_paciente in exclusivosSegundo:
        paciente = historial2_dict[dni_paciente]
        print(f"  {paciente['Nombre']} (DNI: {paciente['DNI']})")

    FuncionesGenerales.pausar()
    FuncionesGenerales.limpiar_pantalla()


def main(): ...


main()
