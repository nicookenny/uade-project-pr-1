import FuncionesGenerales
import Storage
from datetime import date
from functools import reduce


def mostrar_historial(historial):
    for hist_entry in historial:
        resultado = Storage.Pacientes.obtener(hist_entry["paciente_dni"])
        paciente = resultado[1] if resultado else None
        if paciente:
            print(f"DNI: {paciente['DNI']}")
            print(f"  Nombre: {paciente['Nombre']}")
            print(
                f"  Fecha de Nacimiento: {paciente['Fecha de Nacimiento'][2]:02d}/{paciente['Fecha de Nacimiento'][1]:02d}/{paciente['Fecha de Nacimiento'][0]}"
            )
            print(f"  Obra Social: {paciente['Obra Social']}")
            print(
                f"  Fecha Turno: {hist_entry['fecha'][2]:02d}/{hist_entry['fecha'][1]:02d}/{hist_entry['fecha'][0]}"
            )
            print(f"  Estado: {hist_entry['estado']}")
        print("-" * 30)


def mostrar_historial_paginado(historial, cantidad=6):
    total = len(historial)
    inicio = 0
    while inicio < total:
        print("-" * 30)
        fin = min(inicio + cantidad, total)
        for hist_entry in historial[inicio:fin]:
            resultado = Storage.Pacientes.obtener(hist_entry["paciente_dni"])
            paciente = resultado[1] if resultado else None
            if paciente:
                print(f"DNI: {paciente['DNI']}")
                print(f"  Nombre: {paciente['Nombre']}")
                print(
                    f"  Fecha de Nacimiento: {paciente['Fecha de Nacimiento'][2]:02d}/{paciente['Fecha de Nacimiento'][1]:02d}/{paciente['Fecha de Nacimiento'][0]}"
                )
                print(f"  Obra Social: {paciente['Obra Social']}")
                print(
                    f"  Fecha Turno: {hist_entry['fecha'][2]:02d}/{hist_entry['fecha'][1]:02d}/{hist_entry['fecha'][0]}"
                )
                print(f"  Estado: {hist_entry['estado']}")
            print("-" * 30)
        inicio += cantidad
        if inicio < total:
            if not FuncionesGenerales.confirmar_accion(
                "¿Desea ver más historiales?", ""
            ):
                break


def visualizarDatos(lista, Encabezado):
    FuncionesGenerales.limpiar_pantalla()
    print("=" * 40)
    print(f"{Encabezado}")
    print(f"Nombre completo: {lista['Nombre']}")
    print(
        f"Fecha de Nacimiento: {lista['Fecha de Nacimiento'][2]}/{lista['Fecha de Nacimiento'][1]}/{lista['Fecha de Nacimiento'][0]}"
    )
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
    for i, medico in enumerate(Storage.Medicos.listar(), 1):
        hoy = date.today()
        fecha_hoy = (hoy.year, hoy.month, hoy.day)
        turnos_hoy = len(
            [
                t
                for t in Storage.Turnos.listar()
                if t["medico_dni"] == medico["DNI"]
                and t["fecha"] == fecha_hoy
                and t["estado"] == "Confirmado"
            ]
        )
        print(
            f"{i:<3} {medico['Nombre']:<20} {FuncionesGenerales.CalculoEdad(medico['Fecha de Nacimiento']):<12} {medico['DNI']:<10} {medico['Especialidad']:<30} {turnos_hoy:<12}"
        )
    FuncionesGenerales.pausar()


# Funciones de busqueda


def medico_existe(dni):
    return Storage.Medicos.obtener(dni) is not None


def CargaEspecialidad():
    print("=" * 40)
    print("Seleccione una especialidad:")
    for i, especialidad in enumerate(Storage.especialidades_medicas, 1):
        print(f"[{i}] {especialidad}")
    print("=" * 40)

    while True:
        try:
            opcion = int(input("Ingrese el número de la especialidad: "))
            if 1 <= opcion <= len(Storage.especialidades_medicas):
                return Storage.especialidades_medicas[opcion - 1]
            print(
                f"Opción inválida. Debe estar entre 1 y {len(Storage.especialidades_medicas)}"
            )
        except ValueError:
            print("Debe ingresar un número")


def CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad):
    return {
        "Nombre": nombre,
        "Fecha de Nacimiento": FechaDeNacimiento,
        "DNI": dni,
        "Especialidad": Especialidad,
        "Estado": "Disponible",
        "Horarios": {
            "Lunes": (9, 18),
            "Martes": (9, 18),
            "Miércoles": (9, 18),
            "Jueves": (9, 18),
            "Viernes": (9, 18),
            "Sábado": None,
            "Domingo": None,
        },
    }


"""
Opción 2 (menu)
"""


def agregarMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        print("=" * 40)
        MostrartablaMedicos()
        dni = FuncionesGenerales.CargarDNI("medico")

        existe = medico_existe(dni)

        if existe:
            medicoExistente = Storage.Medicos.obtener(dni)
            print(f"El médico {medicoExistente['Nombre']} ya existe")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
        else:
            nombre = FuncionesGenerales.CargarNombre()
            FechaDeNacimiento = FuncionesGenerales.CargarFechaDeNacimiento()
            Especialidad = CargaEspecialidad()
            newMedico = CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad)
            visualizarDatos(newMedico, Encabezado="Resumen de datos del nuevo médico:")
            if not FuncionesGenerales.confirmar_accion(
                "¿Desea confirmar el alta del médico?", "Alta cancelada por el usuario."
            ):
                return

            Storage.Medicos.agregar(newMedico)
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
        dni = FuncionesGenerales.CargarDNI("medico")

        existe = medico_existe(dni)
        if not existe:
            print("El medico no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        medicoExistente = Storage.Medicos.obtener(dni)
        nombre_medico = medicoExistente["Nombre"]
        visualizarDatos(medicoExistente, Encabezado="Datos del medico a eliminar:")
        if not FuncionesGenerales.confirmar_accion(
            "¿Desea confirmar?", "Eliminación cancelada por el usuario."
        ):
            return
        Storage.Medicos.eliminar(dni)
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
        dni = FuncionesGenerales.CargarDNI("medico")

        existe = medico_existe(dni)
        if not existe:
            print("El medico no está en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        medicoExistente = Storage.Medicos.obtener(dni)
        FechaDeNacimiento = FuncionesGenerales.CargarFechaDeNacimiento()
        nombre = FuncionesGenerales.CargarNombre()
        especialidad = CargaEspecialidad()

        new_data = {
            "Nombre": nombre,
            "Fecha de Nacimiento": FechaDeNacimiento,
            "Especialidad": especialidad,
        }

        medicoExistente.update(new_data)
        visualizarDatos(medicoExistente, Encabezado="Datos del medico modificados:")
        if not FuncionesGenerales.confirmar_accion(
            "¿Desea confirmar?", "Modificación cancelada por el usuario."
        ):
            return

        Storage.Medicos.modificar(dni, new_data)
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

    if len(historial) <= 6:
        mostrar_historial(historial)
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

        historial_medico = Storage.Historial.obtener_por_medico(dni)
        if mostrar_opciones_historial(historial_medico):
            return


def mostrarHistorialMedico2():
    FuncionesGenerales.limpiar_pantalla()
    MostrartablaMedicos()

    medico1_dni = int(input("Ingresar numero de documento del primer medico elegido: "))

    medico1Existe = medico_existe(medico1_dni)
    if not medico1Existe:
        print("El primer medico no esta en la lista")
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return

    medico2_dni = int(
        input("Ingresar numero de documento del segundo medico elegido: ")
    )

    medico2Existe = medico_existe(medico2_dni)

    if not medico2Existe:
        print("El segundo medico no esta en la lista")
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return

    if medico1_dni == medico2_dni:
        print("Los medicos son los mismos, eliga otro por favor")
        FuncionesGenerales.pausar()
        return

    FuncionesGenerales.limpiar_pantalla()
    comparacion = Storage.Historial.comparar_medicos(medico1_dni, medico2_dni)

    comunes = comparacion["comunes"]
    exclusivosPrimero = comparacion["solo_medico1"]
    exclusivosSegundo = comparacion["solo_medico2"]

    print("\nPacientes en comun:")
    for dni_paciente in comunes:
        resultado = Storage.Pacientes.obtener(dni_paciente)
        paciente = resultado[1] if resultado else None
        if paciente:
            print(f"  {paciente['Nombre']} (DNI: {paciente['DNI']})")

    print("\nPacientes exclusivos del primero:")
    for dni_paciente in exclusivosPrimero:
        resultado = Storage.Pacientes.obtener(dni_paciente)
        paciente = resultado[1] if resultado else None
        if paciente:
            print(f"  {paciente['Nombre']} (DNI: {paciente['DNI']})")

    print("\nPacientes exclusivos del segundo:")
    for dni_paciente in exclusivosSegundo:
        resultado = Storage.Pacientes.obtener(dni_paciente)
        paciente = resultado[1] if resultado else None
        if paciente:
            print(f"  {paciente['Nombre']} (DNI: {paciente['DNI']})")

    FuncionesGenerales.pausar()
    FuncionesGenerales.limpiar_pantalla()


def buscarMedico():
    medico = FuncionesGenerales.buscar_persona(
        Storage.Medicos.listar(), tipo_busqueda="ambos"
    )
    if medico:
        visualizarDatos(medico, Encabezado="Datos del médico encontrado:")
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return medico
    return None


"""
Opción 7 (menu)
"""


def verTurnosMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        MostrartablaMedicos()
        dni = FuncionesGenerales.CargarDNI("medico")

        existe = medico_existe(dni)
        if not existe:
            print("El medico no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        medico_data = Storage.Medicos.obtener(dni)
        nombre_medico = medico_data["Nombre"]

        turnos_filtrados = filter(
            lambda t: t["medico_dni"] == dni and t["estado"] == "Confirmado",
            Storage.Turnos.listar(),
        )
        total_turnos = reduce(lambda count, turno: count + 1, turnos_filtrados, 0)

        print("=" * 40)
        print(f"Médico: {nombre_medico}")
        print(f"DNI: {dni}")
        print(f"Total de turnos confirmados: {total_turnos}")
        print("=" * 40)
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return


def main(): ...


main()
