import os
import Datos
from datetime import date
from functools import reduce

def mostrar_historial(historial):
    for paciente in historial:
        for dni, datos in paciente.items():
            print(f"DNI: {dni}")
            print(f"  Nombre: {datos['Nombre']}")
            print(f"  Fecha de Nacimiento: {datos['Fecha de Nacimiento'][2]:02d}/{datos['Fecha de Nacimiento'][1]:02d}/{datos['Fecha de Nacimiento'][0]}")
            print(f"  Obra Social: {datos['Obra Social']}")
            print("-" * 30)


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresione Enter para continuar...")


def CalculoEdad(fecha):
    hoy = date.today()
    año, mes, dia = fecha
    edad = hoy.year - año - ((hoy.month, hoy.day) < (mes, dia))
    return edad


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


def medico_disponible(datos_medico):
    return datos_medico["Paciente"] == {}


def MostrartablaMedicos():
    limpiar_pantalla()
    print(
        f"{'ID':<3} {'Nombre':<20} {'Edad':<12} {'DNI':<10} {'Especialidad':<30} {'Estado':<12} {'Paciente'}"
    )
    print("-" * 102)
    for i, medico in enumerate(Datos.medicos, 1):
        print(
            f"{i:<3} {medico['Nombre']:<20} {CalculoEdad(medico['Fecha de Nacimiento']):<12} {medico['DNI']:<10} {medico['Especialidad']:<30} {medico['Estado']:<12} {medico['Paciente']}"
        )
    pausar()


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
    nombre = input("Ingresar el nombre: ")
    while nombre == "" or nombre.isnumeric():
        print("Nombre no válido")
        nombre = input("Ingrese otro nombre: ")
    return nombre


def CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad):
    return {
        "Nombre": nombre,
        "Fecha de Nacimiento": FechaDeNacimiento,
        "DNI": dni,
        "Especialidad": Especialidad,
        "Estado": "Disponible",
        "Paciente": {},
        "Historial": [],
    }


def agregarMedico():
    limpiar_pantalla()
    while True:
        print("=" * 40)
        MostrartablaMedicos()
        dni = CargarDNI()

        existe = medico_existe(dni)

        if existe:
            medicoExistente = buscar_medico_por_dni(dni)
            print(f"El médico {medicoExistente['Nombre']} ya existe")
            pausar()
            limpiar_pantalla()
        else:
            nombre = CargarNombre()
            FechaDeNacimiento = CargarFechaDeNacimiento()
            Especialidad = CargaEspecialidad()
            Datos.medicos.append(
                CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad)
            )
            print("El medico se agregó correctamente")
            pausar()
            break

    MostrartablaMedicos()
    limpiar_pantalla()


def eliminarMedico():
    limpiar_pantalla()
    while True:
        MostrartablaMedicos()
        print()
        print("=" * 40)
        dni = CargarDNI()

        existe = medico_existe(dni)
        if not existe:
            print("El medico no esta en la lista")
            pausar()
            limpiar_pantalla()
            continue

        medicoExistente = buscar_medico_por_dni(dni)
        if not medico_disponible(medicoExistente):
            print("El medico tiene informacion importante y no puede ser eliminado")
            pausar()
            limpiar_pantalla()
            continue

        nombre_medico = medicoExistente["Nombre"]
        index = Datos.medicos.index(medicoExistente)
        del Datos.medicos[index]
        print(f"El medico {nombre_medico} se elimino correctamente de la lista")
        pausar()
        MostrartablaMedicos()
        return


def modificarMedico():
    limpiar_pantalla()
    while True:
        MostrartablaMedicos()
        dni = CargarDNI()

        existe = medico_existe(dni)
        if not existe:
            print("El medico no está en la lista")
            pausar()
            limpiar_pantalla()
            continue

        medicoExistente = buscar_medico_por_dni(dni)
        if not medico_disponible(medicoExistente):
            print("El medico tiene información importante y no puede ser modificado")
            pausar()
            limpiar_pantalla()
            continue

        FechaDeNacimiento = CargarFechaDeNacimiento()
        nombre = CargarNombre()
        especialidad = CargaEspecialidad()

        medicoExistente["Nombre"] = nombre
        medicoExistente["Fecha de Nacimiento"] = FechaDeNacimiento
        medicoExistente["Especialidad"] = especialidad

        print("Se han modificado sus datos correctamente\n")
        MostrartablaMedicos()
        limpiar_pantalla()
        return


def mostrarHistorialMedico():
    limpiar_pantalla()
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
            pausar()
            limpiar_pantalla()


def mostrar_opciones_historial(historial):
    if not historial:
        print("El medico no tiene historial clinico")
        pausar()
        limpiar_pantalla()
        return True

    if len(historial) < 3:
        print(f"\n{historial}")
        pausar()
        limpiar_pantalla()
        return True

    print("\n" + "=" * 40)
    print("[1] Mostrar los primeros 6 pacientes")
    print("[2] Mostrar todo el historial Medico")
    opcion = int(input("Ingresar una Opcion: "))

    if opcion == 1:
        mostrar_historial(historial[:6])
    elif opcion == 2:
        mostrar_historial(historial)
    else:
        print("Opcion incorrecta")

    pausar()
    limpiar_pantalla()
    return True


def mostrarHistorialMedico1():
    while True:
        MostrartablaMedicos()
        dni = int(input("Ingresar numero de documento del Medico: "))

        existe = medico_existe(dni)
        if not existe:
            print("El medico no esta en la lista")
            pausar()
            limpiar_pantalla()
            continue

        medicoExistente = buscar_medico_por_dni(dni)
        if mostrar_opciones_historial(medicoExistente["Historial"]):
            return


def obtener_historial_dict(id_medico):
    historial_dict = {}
    if 0 <= id_medico < len(Datos.medicos):
        for paciente in Datos.medicos[id_medico]["Historial"]:
            historial_dict.update(paciente)
    return historial_dict


def mostrarHistorialMedico2():
    limpiar_pantalla()
    MostrartablaMedicos()

    medico1_dni = int(input("Ingresar numero de documento del primer medico elegido: "))

    medico1Existe = medico_existe(medico1_dni)
    if not medico1Existe:
        print("El primer medico no esta en la lista o su historial esta vacio")
        pausar()
        limpiar_pantalla()
        return

    medico2_dni = int(
        input("Ingresar numero de documento del segundo medico elegido: ")
    )

    medico2Existe = medico_existe(medico2_dni)

    if not medico2Existe:
        print("El segundo medico no esta en la lista o su historial esta vacio")
        pausar()
        limpiar_pantalla()
        return

    if medico1_dni == medico2_dni:
        print("Los medicos son los mismos, eliga otro por favor")
        pausar()
        return

    limpiar_pantalla()
    historial1_dict = obtener_historial_dict(medico1_dni)
    historial2_dict = obtener_historial_dict(medico2_dni)

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

    pausar()
    limpiar_pantalla()


def main(): ...


main()
