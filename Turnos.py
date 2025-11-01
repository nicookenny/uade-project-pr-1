import FuncionesGenerales
import Datos
import Medicos
import Pacientes
from datetime import date, timedelta

def buscar_paciente(dni_paciente):
    for paciente in Datos.pacientes:
        if paciente["DNI"] == dni_paciente:
            return paciente
    return None


def buscar_medico_por_dni(dni_medico):
    for medico in Datos.medicos:
        if medico["DNI"] == dni_medico:
            return medico
    return None


def generar_id_turno():
    if not Datos.turnos:
        return 1
    return max(t["id"] for t in Datos.turnos) + 1


def obtener_dia_semana(fecha):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    fecha_obj = date(fecha[0], fecha[1], fecha[2])
    return dias[fecha_obj.weekday()]


def obtener_slots_disponibles(medico_dni, fecha):
    medico = buscar_medico_por_dni(medico_dni)
    if not medico:
        return []

    dia_semana = obtener_dia_semana(fecha)
    horario = medico["Horarios"].get(dia_semana)

    if not horario:
        return []

    hora_inicio, hora_fin = horario
    slots = []

    hora = hora_inicio
    minuto = 0
    while hora < hora_fin or (hora == hora_fin and minuto == 0):
        slot = (hora, minuto)
        ocupado = any(
            t["medico_dni"] == medico_dni and
            t["fecha"] == fecha and
            t["hora"] == slot and
            t["estado"] == "Confirmado"
            for t in Datos.turnos
        )
        if not ocupado:
            slots.append(slot)

        minuto += 30
        if minuto >= 60:
            minuto = 0
            hora += 1

    if slots and slots[-1][0] >= hora_fin:
        slots.pop()

    return slots


def buscar_turnos_paciente(dni_paciente):
    return [t for t in Datos.turnos if t["paciente_dni"] == dni_paciente and t["estado"] == "Confirmado"]


def mostrar_turnos_paciente(dni_paciente):
    turnos = buscar_turnos_paciente(dni_paciente)
    if not turnos:
        print("El paciente no tiene turnos agendados")
        return

    print("\nTurnos del paciente:")
    print(f"{'ID':<5} {'Médico':<20} {'Especialidad':<30} {'Fecha':<12} {'Hora':<8}")
    print("-" * 85)

    for turno in turnos:
        medico = buscar_medico_por_dni(turno["medico_dni"])
        fecha_str = f"{turno['fecha'][2]:02d}/{turno['fecha'][1]:02d}/{turno['fecha'][0]}"
        hora_str = f"{turno['hora'][0]:02d}:{turno['hora'][1]:02d}"
        print(
            f"{turno['id']:<5} {medico['Nombre']:<20} {medico['Especialidad']:<30} {fecha_str:<12} {hora_str:<8}"
        )


def verTurnosPaciente():
    while True:
        Pacientes.mostrarLista()
        #print("Ingrese el DNI del paciente para ver sus turnos->")
        dni_paciente = FuncionesGenerales.CargarDNI("paciente para ver sus turnos")
        paciente_data = buscar_paciente(dni_paciente)

        if not paciente_data:
            print("El paciente no existe en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        FuncionesGenerales.limpiar_pantalla()
        print(f"\nTurnos de {paciente_data['Nombre']} (DNI: {dni_paciente})")
        print("=" * 85)
        mostrar_turnos_paciente(dni_paciente)
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return


def buscar_turnos_medico(dni_medico):
    return [t for t in Datos.turnos if t["medico_dni"] == dni_medico and t["estado"] == "Confirmado"]


def mostrar_turnos_medico(dni_medico):
    turnos = buscar_turnos_medico(dni_medico)
    if not turnos:
        print("El médico no tiene turnos agendados")
        return

    turnos_ordenados = sorted(turnos, key=lambda t: (t["fecha"], t["hora"]))

    print("\nTurnos del médico:")
    print(f"{'ID':<5} {'Paciente':<20} {'Fecha':<12} {'Hora':<8} {'DNI Paciente':<12}")
    print("-" * 70)

    for turno in turnos_ordenados:
        paciente = buscar_paciente(turno["paciente_dni"])
        fecha_str = f"{turno['fecha'][2]:02d}/{turno['fecha'][1]:02d}/{turno['fecha'][0]}"
        hora_str = f"{turno['hora'][0]:02d}:{turno['hora'][1]:02d}"
        print(
            f"{turno['id']:<5} {paciente['Nombre']:<20} {fecha_str:<12} {hora_str:<8} {paciente['DNI']:<12}"
        )


def verTurnosMedico():
    while True:
        Medicos.MostrartablaMedicos()
        #print("Ingrese el DNI del médico para ver sus turnos->")
        dni_medico = FuncionesGenerales.CargarDNI("médico para ver sus turnos")
        medico_data = buscar_medico_por_dni(dni_medico)

        if not medico_data:
            print("El médico no existe en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        FuncionesGenerales.limpiar_pantalla()
        print(f"\nAgenda de {medico_data['Nombre']} - {medico_data['Especialidad']}")
        print("=" * 70)
        mostrar_turnos_medico(dni_medico)
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return


def mostrar_calendario_disponibilidad(medico_dni, medico_data):
    hoy = date.today()
    meses_a_mostrar = {}

    for i in range(30):
        fecha_futura = hoy + timedelta(days=i)
        fecha_tuple = (fecha_futura.year, fecha_futura.month, fecha_futura.day)
        dia_semana = obtener_dia_semana(fecha_tuple)
        horario = medico_data["Horarios"].get(dia_semana)

        mes_año = (fecha_futura.year, fecha_futura.month)
        if mes_año not in meses_a_mostrar:
            meses_a_mostrar[mes_año] = {}

        if horario:
            slots = obtener_slots_disponibles(medico_dni, fecha_tuple)
            meses_a_mostrar[mes_año][fecha_futura.day] = len(slots) if slots else 0
        else:
            meses_a_mostrar[mes_año][fecha_futura.day] = -1

    meses_nombres = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    for mes_año, dias_info in meses_a_mostrar.items():
        año, mes = mes_año
        print(f"\n        {meses_nombres[mes]} {año}")
        print("  L      M      X      J      V      S      D")

        primer_dia = date(año, mes, 1)
        dia_semana_inicio = primer_dia.weekday()

        if mes == 12:
            ultimo_dia = 31
        else:
            ultimo_dia = (date(año, mes + 1, 1) - timedelta(days=1)).day

        semana = []
        for _ in range(dia_semana_inicio):
            semana.append("       ")

        for dia in range(1, ultimo_dia + 1):
            if dia in dias_info:
                if dias_info[dia] == -1:
                    semana.append(f"{dia:2d}(-)".ljust(7))
                elif dias_info[dia] == 0:
                    semana.append(f"{dia:2d}(-)".ljust(7))
                else:
                    semana.append(f"{dia:2d}({dias_info[dia]:2d})".ljust(7))
            else:
                if dia < hoy.day and mes == hoy.month and año == hoy.year:
                    semana.append("       ")
                else:
                    semana.append("       ")

            if len(semana) == 7:
                print("".join(semana))
                semana = []

        if semana:
            while len(semana) < 7:
                semana.append("       ")
            print("".join(semana))

    print("\nDD(N) = Día DD con N turnos disponibles  |  DD(-) = No disponible")


def agendarTurno():
    while True:
        Pacientes.mostrarLista()
        #print("Ingrese el DNI del paciente que quiere agendar el turno->")
        dni_paciente = FuncionesGenerales.CargarDNI("paciente que quiere agendar el turno")
        paciente_data = buscar_paciente(dni_paciente)

        if not paciente_data:
            print("El paciente no existe en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        Pacientes.visualizarDatos(paciente_data, Encabezado="Datos del paciente seleccionado")
        confirmar = input("\n¿Desea continuar? (s/n) [s]: ").lower() or "s"
        if confirmar != "s":
            print("Acción cancelada por el usuario.")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return

        while True:
            Medicos.MostrartablaMedicos()
            #print("Ingrese el DNI del medico->")
            dni_medico = FuncionesGenerales.CargarDNI("medico")
            medico_data = buscar_medico_por_dni(dni_medico)

            if not medico_data:
                print("El medico no esta en la lista")
                FuncionesGenerales.pausar()
                FuncionesGenerales.limpiar_pantalla()
                continue

            print(f"\nMédico seleccionado: {medico_data['Nombre']} - {medico_data['Especialidad']}")

            print("\nCalendario de Turnos Disponibles (próximos 30 días):")
            mostrar_calendario_disponibilidad(dni_medico, medico_data)

            hoy = date.today()

            while True:
                fecha_input = input("\nIngrese la fecha (DD-MM-YYYY): ")

                try:
                    partes = fecha_input.split("-")
                    if len(partes) != 3:
                        print("Formato inválido. Use DD-MM-YYYY")
                        FuncionesGenerales.pausar()
                        continue

                    dia = int(partes[0])
                    mes = int(partes[1])
                    año = int(partes[2])

                    fecha_turno = date(año, mes, dia)
                    fecha_tuple = (año, mes, dia)

                    if fecha_turno < hoy:
                        print("La fecha no puede ser anterior a hoy")
                        FuncionesGenerales.pausar()
                        continue

                    if fecha_turno > hoy + timedelta(days=30):
                        print("Solo puede agendar turnos con hasta 30 días de anticipación")
                        FuncionesGenerales.pausar()
                        continue

                    slots = obtener_slots_disponibles(dni_medico, fecha_tuple)

                    if not slots:
                        print(f"El médico no tiene disponibilidad para el día {obtener_dia_semana(fecha_tuple)}")
                        FuncionesGenerales.pausar()
                        continue

                    print(f"\nTurnos disponibles para el {dia:02d}/{mes:02d}/{año}:")
                    print("-" * 50)

                    for i, slot in enumerate(slots, 1):
                        print(f"[{i}] {slot[0]:02d}:{slot[1]:02d}", end="  ")
                        if i % 4 == 0:
                            print()
                    print("\n" + "-" * 50)

                    opcion = int(input("Seleccione el número del turno: "))

                    if opcion < 1 or opcion > len(slots):
                        print("Opción inválida")
                        FuncionesGenerales.pausar()
                        continue

                    hora_seleccionada = slots[opcion - 1]

                    print("\n" + "=" * 40)
                    print("Resumen del turno a agendar:")
                    print(f"Paciente: {paciente_data['Nombre']} (DNI: {paciente_data['DNI']})")
                    print(f"Médico: {medico_data['Nombre']} (DNI: {medico_data['DNI']})")
                    print(f"Especialidad: {medico_data['Especialidad']}")
                    print(f"Fecha: {dia:02d}/{mes:02d}/{año}")
                    print(f"Hora: {hora_seleccionada[0]:02d}:{hora_seleccionada[1]:02d}")
                    print("=" * 40)

                    confirmar_turno = input("¿Desea confirmar el turno? (s/n) [s]: ").lower() or "s"
                    if confirmar_turno != "s":
                        print("Turno cancelado por el usuario.")
                        FuncionesGenerales.pausar()
                        FuncionesGenerales.limpiar_pantalla()
                        return

                    nuevo_turno = {
                        "id": generar_id_turno(),
                        "medico_dni": dni_medico,
                        "paciente_dni": dni_paciente,
                        "fecha": fecha_tuple,
                        "hora": hora_seleccionada,
                        "estado": "Confirmado"
                    }

                    Datos.turnos.append(nuevo_turno)

                    medico_data["Historial"].append({
                        "DNI": paciente_data["DNI"],
                        "Nombre": paciente_data["Nombre"],
                        "Fecha de Nacimiento": paciente_data["Fecha de Nacimiento"],
                        "Obra Social": paciente_data["Obra Social"],
                        "Fecha Turno": fecha_tuple
                    })

                    print("\nEl turno se agendó correctamente")
                    FuncionesGenerales.pausar()
                    FuncionesGenerales.limpiar_pantalla()
                    return

                except Exception as e:
                    print("Fecha inválida")
                    FuncionesGenerales.pausar()
                    FuncionesGenerales.registrarErrores(e)
                    continue


def cancelarTurno():
    while True:
        Pacientes.mostrarLista()
        #print("Ingrese el DNI del paciente que quiere cancelar el turno->")
        dni_paciente = FuncionesGenerales.CargarDNI("paciente que quiere cancelar el turno")
        paciente_data = buscar_paciente(dni_paciente)

        if not paciente_data:
            print("El paciente no existe en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return

        turnos = buscar_turnos_paciente(dni_paciente)

        if not turnos:
            print("El paciente no tiene turnos agendados")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return

        FuncionesGenerales.limpiar_pantalla()
        mostrar_turnos_paciente(dni_paciente)

        print("\nIngrese el ID del turno a cancelar->")
        id_turno = int(input())

        turno_encontrado = None
        for turno in Datos.turnos:
            if turno["id"] == id_turno and turno["paciente_dni"] == dni_paciente and turno["estado"] == "Confirmado":
                turno_encontrado = turno
                break

        if not turno_encontrado:
            print("Turno no encontrado o ya cancelado")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return

        medico_data = buscar_medico_por_dni(turno_encontrado["medico_dni"])

        print("\n" + "=" * 40)
        print("Resumen del turno a cancelar:")
        print(f"Paciente: {paciente_data['Nombre']} (DNI: {paciente_data['DNI']})")
        print(f"Médico: {medico_data['Nombre']} (DNI: {medico_data['DNI']})")
        print(f"Especialidad: {medico_data['Especialidad']}")
        print(f"Fecha: {turno_encontrado['fecha'][2]:02d}/{turno_encontrado['fecha'][1]:02d}/{turno_encontrado['fecha'][0]}")
        print(f"Hora: {turno_encontrado['hora'][0]:02d}:{turno_encontrado['hora'][1]:02d}")
        print("=" * 40)

        confirmar = input("¿Desea cancelar el turno? (s/n) [s]: ").lower() or "s"
        if confirmar != "s":
            print("Cancelación abortada por el usuario.")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return

        turno_encontrado["estado"] = "Cancelado"

        print("\nEl turno se canceló correctamente")
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return


def main():
    pass


main()
