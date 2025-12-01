import FuncionesGenerales as FG
import menues

def main():
    menu_principal = {
        "1": {"text": "Gestión de Médicos", "action": lambda: menues.ejecutar_menu(menues.menu_medicos, "MÉDICOS")},
        "2": {"text": "Gestión de Pacientes", "action": lambda: menues.ejecutar_menu(menues.menu_pacientes, "PACIENTES")},
        "3": {"text": "Gestión de Turnos", "action": lambda: menues.ejecutar_menu(menues.menu_turnos, "TURNOS")},
        "0": {"text": "Salir", "action": None},
    }

    while True:
        FG.limpiar_pantalla()
        print("========================================")
        print("   SISTEMA DE GESTIÓN HOSPITALARIA")
        print("========================================")
        
        menues.mostrar_menu(menu_principal, "MENÚ PRINCIPAL")
        
        op = input("\nIngrese su opción: ").strip()
        
        if op == "0":
            print("\nGuardando datos y saliendo...")
            break
        elif op in menu_principal:
            menu_principal[op]["action"]()
        else:
            print("Opción inválida.")
            FG.pausar()

if __name__ == "__main__":
   main()
   