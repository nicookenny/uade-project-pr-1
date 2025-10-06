import FuncionesGenerales
import Datos
import Medicos
import Pacientes

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
        print("Ingrese el DNI del paciente que quiere agregar el turno->")
        dni_paciente = FuncionesGenerales.CargarDNI()
        paciente_data = buscar_paciente(dni_paciente)

        if not paciente_data:
            print("El paciente no existe en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        if paciente_tiene_turno(dni_paciente):
            print("El paciente ya tiene un turno agendado con otro médico.")
            FuncionesGenerales.pausar()
            return

        # Mostrar datos del paciente seleccionado
        Pacientes.visualizarDatos(paciente_data,Encabezado="Datos del paciente seleccionado")
        confirmar = input("\n¿Desea continuar? (s/n): ").lower()
        if confirmar != "s":
            print("Acción cancelada por el usuario.")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return

        while True:
            Medicos.MostrartablaMedicos()
            print("Ingrese el DNI del medico que quiere agregar el turno->")
            dni_medico=FuncionesGenerales.CargarDNI()
            medico_data = buscar_medico_por_dni(dni_medico)

            if not medico_data:
                print("El medico no esta en la lista")
                FuncionesGenerales.pausar()
                FuncionesGenerales.limpiar_pantalla()
                continue

            if medico_data["Estado"] == "Disponible":
                # Mostrar resumen antes de guardar
                print(" ")
                print("=" * 40)
                print("Resumen del turno a agendar:")
                print(f"Paciente: {paciente_data['Nombre']} (DNI: {paciente_data['DNI']})")
                print(f"Médico: {medico_data['Nombre']} (DNI: {medico_data['DNI']})")
                print(f"Especialidad: {medico_data['Especialidad']}")
                print("=" * 40)
                confirmar = input("¿Desea confirmar el turno? (s/n): ").lower()
                if confirmar != "s":
                    print("Turno cancelado por el usuario.")
                    FuncionesGenerales.pausar()
                    FuncionesGenerales.limpiar_pantalla()
                    return

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
                FuncionesGenerales.pausar()
                Medicos.MostrartablaMedicos()
                return
            else:
                print("El medico esta ocupado")
                FuncionesGenerales.pausar()
                FuncionesGenerales.limpiar_pantalla() 


def cancelarTurno():
    while True:
        Pacientes.mostrarLista()
        print("Ingrese el DNI del paciente que quiere cancelar el turno->")
        dni_paciente = FuncionesGenerales.CargarDNI()
        paciente_data = buscar_paciente(dni_paciente)

        if not paciente_data:
            print("El paciente no existe en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return

        if not paciente_tiene_turno(dni_paciente):
            print("El paciente no agendo nunca un turno")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return

        while True:
            Medicos.MostrartablaMedicos()
            print("Ingrese el DNI del medico que quiere cancelar el turno->")
            dni_medico = FuncionesGenerales.CargarDNI()
            medico_data = buscar_medico_por_dni(dni_medico)

            if not medico_data:
                print("El medico no esta en la lista")
                FuncionesGenerales.pausar()
                FuncionesGenerales.limpiar_pantalla()
                return

            if medico_data["Estado"] == "Disponible":
                print("ERROR, el medico esta disponible")
                FuncionesGenerales.pausar()
                FuncionesGenerales.limpiar_pantalla()
                return

            if buscar_turno_paciente_con_medico(dni_paciente, dni_medico):
                print("\nDatos del paciente:")
                print(f"Nombre: {paciente_data['Nombre']}")
                print(f"DNI: {paciente_data['DNI']}")
                print("=" * 40)
                print("Datos del médico:")
                print(f"Nombre: {medico_data['Nombre']}")
                print(f"DNI: {medico_data['DNI']}")
                print(f"Especialidad: {medico_data['Especialidad']}")
                print("=" * 40)
                print(f"Turno: {medico_data['Especialidad']}")
                print("=" * 40)
                confirmar = input("¿Desea cancelar el turno? (s/n): ").lower()
                if confirmar != "s":
                    print("Cancelación abortada por el usuario.")
                    FuncionesGenerales.pausar()
                    FuncionesGenerales.limpiar_pantalla()
                    return
                
                medico_data["Estado"] = "Disponible"
                medico_data["Paciente"] = {}

                print("El turno se cancelo correctamente")
                FuncionesGenerales.pausar()
                Medicos.MostrartablaMedicos()
                FuncionesGenerales.limpiar_pantalla()
                return
            else:
                print("El medico esta agendado con otro paciente")
                FuncionesGenerales.pausar()
                return


def main():
    pass


main()
