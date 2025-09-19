import Medicos
import Pacientes
import Turnos

doctors_menu = {
    "0": {
        "text": "Salir del programa",
        "action": Medicos.MostrartablaMedicos,
    },
    "1": {
        "text": "Ver medicos",
        "action": Medicos.MostrartablaMedicos,
    },
    "2": {
        "text": "Agregar medico",
        "action": Medicos.agregarMedico,
    },
    "3": {
        "text": "Eliminar medico",
        "action": Medicos.eliminarMedico,
    },
    "4": {
        "text": "Modificar medico",
        "action": Medicos.modificarMedico,
    },
    "5": {
        "text": "Mostrar historial de un medico",
        "action": Medicos.mostrarHistorialMedico,
    },
}

patients_menu = {
    "0": {
        "text": "Salir del programa",
        "action": lambda: exit(),
    },
    "1": {
        "text": "Ver pacientes",
        "action": Pacientes.mostrarLista,
    },
    "2": {
        "text": "Agregar Paciente",
        "action": Pacientes.agregarPaciente,
    },
    "3": {
        "text": "Eliminar Paciente",
        "action": Pacientes.eliminarPaciente,
    },
    "4": {
        "text": "Modificar Paciente",
        "action": Pacientes.modificarPaciente,
    },
}


turns_menu = {
    "0": {
        "text": "Volver al menu principal",
        "action": None,
    },
    "1": {
        "text": "Agendar Turno",
        "action": Turnos.agendarTurno,
    },
    "2": {
        "text": "Cancelar Turno",
        "action": Turnos.cancelarTurno,
    },
}


def showMenu(menu, title):
    print(title)
    for key, value in menu.items():
        print(f"[{key}] {value['text']}")
