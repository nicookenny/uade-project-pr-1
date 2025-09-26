import os
import Datos
import Medicos
import Pacientes


def CargarDNI():
    dni = input("Ingresar número de documento: ")
    while not dni.isdigit() or len(dni) != 8:
        print("DNI inválido")
        dni = input("Ingresar otro número de documento: ")
    return int(dni)


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresione Enter para continuar...")


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


def paciente_tiene_turno(dni_paciente):
    for medico in Datos.medicos:
        if medico["Paciente"] and medico["Paciente"]["DNI"] == dni_paciente:
            return True
    return False


def buscar_turno_paciente_con_medico(dni_paciente, dni_medico):
    medico_data = buscar_medico_por_dni(dni_medico)
    if not medico_data:
        return False

    return medico_data["Paciente"] and medico_data["Paciente"]["DNI"] == dni_paciente


def agendarTurno():
    while True:
        Pacientes.mostrarLista()
        dni_paciente = CargarDNI()
        paciente_data = buscar_paciente(dni_paciente)

        if not paciente_data:
            print("El paciente no existe en la lista")
            pausar()
            limpiar_pantalla()
            continue

        if paciente_tiene_turno(dni_paciente):
            print("El paciente ya tiene un turno agendado con otro médico.")
            pausar()
            return

        while True:
            Medicos.MostrartablaMedicos()
            dni_medico = int(
                input(
                    "Ingresar numero de documento del medico con el que queres agendar un turno: "
                )
            )
            medico_data = buscar_medico_por_dni(dni_medico)

            if not medico_data:
                print("El medico no esta en la lista")
                pausar()
                limpiar_pantalla()
                continue

            if medico_data["Estado"] == "Disponible":
                medico_data["Estado"] = "Ocupado"
                medico_data["Paciente"] = paciente_data
                medico_data["Historial"].append(
                    {
                        paciente_data["DNI"]: {
                            "Nombre": paciente_data["Nombre"],
                            "Fecha de Nacimiento": paciente_data["Fecha de Nacimiento"],
                            "Obra Social": paciente_data["Obra Social"],
                        }
                    }
                )
                print("El turno se agendo correctamente")
                pausar()
                Medicos.MostrartablaMedicos()
                return
            else:
                print("El medico esta ocupado")
                pausar()
                limpiar_pantalla()


def cancelarTurno():
    while True:
        Pacientes.mostrarLista()
        dni_paciente = CargarDNI()
        paciente_data = buscar_paciente(dni_paciente)

        if not paciente_data:
            print("El paciente no existe en la lista")
            pausar()
            limpiar_pantalla()
            return

        if not paciente_tiene_turno(dni_paciente):
            print("El paciente no agendo nunca un turno")
            pausar()
            limpiar_pantalla()
            return

        while True:
            Medicos.MostrartablaMedicos()
            dni_medico = CargarDNI()
            medico_data = buscar_medico_por_dni(dni_medico)

            if not medico_data:
                print("El medico no esta en la lista")
                pausar()
                limpiar_pantalla()
                return

            if medico_data["Estado"] == "Disponible":
                print("ERROR, el medico esta disponible")
                pausar()
                limpiar_pantalla()
                return

            if buscar_turno_paciente_con_medico(dni_paciente, dni_medico):
                medico_data["Estado"] = "Disponible"
                medico_data["Paciente"] = {}
                print("El turno se cancelo correctamente")
                pausar()
                Medicos.MostrartablaMedicos()
                return
            else:
                print("El medico esta agendado con otro paciente")
                pausar()
                return


def main():
    pass


main()
