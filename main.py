import FuncionesGenerales
from menues import showMenu, doctors_menu, patients_menu, turns_menu


def menuMedicos():  # Menu de los medicos
    FuncionesGenerales.limpiar_pantalla()
    """
    Menu en donde se puede eliminar,agregar o modificar la lista de los medicos, donde estos mismos estan en una matriz(lista) de diccionarios
    """
    while True:
        showMenu(doctors_menu, title="Menu de Medicos")
        opcion = input("Ingresar una Opcion: ")

        if opcion == "0":
            menuHospital()
            return

        if opcion in doctors_menu:
            doctors_menu[opcion]["action"]()
        else:
            print("Opcion Invalida, Ingrese nuevamente los datos:")
            input("\nPresione Enter para continuar...")


def menuPacientes():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        showMenu(patients_menu, title="Menu de Pacientes")
        opcion = input("Ingresar una Opcion: ")
        if opcion == "0":
            menuHospital()
            return

        if opcion in patients_menu:
            patients_menu[opcion]["action"]()
        else:
            print("Opcion Invalida, Ingrese nuevamente los datos:")
            input("\nPresione Enter para continuar...")


def menuTurnos():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        showMenu(turns_menu, title="Menu de Turnos")
        opcion = input("Ingresar una Opcion: ")

        if opcion == "0":
            menuHospital()
            return

        if opcion in turns_menu:
            turns_menu[opcion]["action"]()
        else:
            print("Opcion Invalida, Ingrese nuevamente los datos:")
            input("\nPresione Enter para continuar...")


main_menu = {
    "0": {
        "text": "Salir del programa",
        "action": lambda: exit(),
    },
    "1": {
        "text": "Mostrar Menu de Medico",
        "action": menuMedicos,
    },
    "2": {
        "text": "Mostrar Menu de Paciente",
        "action": menuPacientes,
    },
    "3": {
        "text": "Mostrar Menu de Turno",
        "action": menuTurnos,
    },
}


def menuHospital():  # Menu principal
    FuncionesGenerales.limpiar_pantalla()
    while True:
        showMenu(main_menu, title="Menu Principal")
        opcion = input("Ingresar una Opcion: ")

        if opcion in main_menu:
            main_menu[opcion]["action"]()
        else:
            print("Opcion Invalida, Ingrese nuevamente los datos:")
            input("\nPresione Enter para continuar...")


def main():
    menuHospital()
    FuncionesGenerales.limpiar_pantalla()
    print("Saliendo del programa...")


main()
