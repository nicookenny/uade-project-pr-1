import Medicos
import Pacientes
import Turnos

# Estructura simple de diccionarios para menús

menu_medicos = {
    "1": {"text": "Ver lista de médicos", "action": Medicos.mostrar_tabla_medicos},
    "2": {"text": "Agregar médico", "action": Medicos.agregar_medico},
    "3": {"text": "Modificar médico", "action": Medicos.modificar_medico},
    "4": {"text": "Eliminar médico", "action": Medicos.eliminar_medico},
    "5": {"text": "Buscar médico", "action": Medicos.buscar_medico},
    "6": {"text": "Historiales / Comparación", "action": Medicos.mostrar_historial_medico},
    "7": {"text": "Ver estadísticas (Turnos)", "action": Medicos.ver_turnos_medico},
    "0": {"text": "Volver", "action": None},
}

menu_pacientes = {
    "1": {"text": "Ver lista de pacientes", "action": Pacientes.mostrar_lista_pacientes},
    "2": {"text": "Agregar paciente", "action": Pacientes.agregar_paciente},
    "3": {"text": "Modificar paciente", "action": Pacientes.modificar_paciente},
    "4": {"text": "Eliminar paciente", "action": Pacientes.eliminar_paciente},
    "5": {"text": "Buscar paciente", "action": Pacientes.buscar_paciente},
    "6": {"text": "Ver mis turnos", "action": Turnos.ver_turnos_paciente},
    "0": {"text": "Volver", "action": None},
}

menu_turnos = {
    "1": {"text": "Agendar Turno", "action": Turnos.agendar_turno},
    "2": {"text": "Cancelar Turno", "action": Turnos.cancelar_turno},
    "3": {"text": "Ver Turnos por Paciente", "action": Turnos.ver_turnos_paciente},
    "0": {"text": "Volver", "action": None},
}

def mostrar_menu(opciones, titulo):
    print(f"\n=== {titulo} ===")
    for k, v in opciones.items():
        print(f"[{k}] {v['text']}")

def ejecutar_menu(opciones, titulo):
    while True:
        import FuncionesGenerales as FG
        FG.limpiar_pantalla()
        mostrar_menu(opciones, titulo)
        op = input("\nIngrese su opción: ").strip()
        
        if op in opciones:
            accion = opciones[op]["action"]
            if accion is None: # Caso "Volver" o "Salir"
                return
            accion()
        else:
            print("Opción inválida.")
            FG.pausar()