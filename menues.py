import Medicos
import Pacientes
import Turnos

doctors_menu = {
    "0": {
        "text": "Volver al menu principal",
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
    "6": {
        "text": "Buscar medico",
        "action": Medicos.buscarMedico,
    },
    "7": {
        "text": "Ver cantidad de turnos de un medico",
        "action": Medicos.verTurnosMedico,
    },
}

patients_menu = {
    "0": {
        "text": "Volver al menu principal",
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
    "5": {
        "text": "Ver turnos de un paciente",
        "action": Turnos.verTurnosPaciente,
    },
    "6": {
        "text": "Buscar paciente",
        "action": Pacientes.buscarPaciente,
    },
}


turns_menu = {
    "0": {
        "text": "Volver al menu principal",
        "action": lambda: None,
    },
    "1": {
        "text": "Agendar Turno",
        "action": Turnos.agendarTurno,
    },
    "2": {
        "text": "Cancelar Turno",
        "action": Turnos.cancelarTurno,
    },
    "3": {
        "text":"Mostrar Turnos",
        "action": Turnos.verTurnosPaciente,
    }
}


def showMenu(menu, title):
    print(title)
    for key, value in menu.items():
        print(f"[{key}] {value['text']}")
