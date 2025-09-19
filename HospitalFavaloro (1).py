import os
import sys
import time
import Medicos
import Pacientes
import Turnos

                        

def menuMedicos(): # Menu de los medicos
    os.system('cls')
    """
    Menu en donde se puede eliminar,agregar o modificar la lista de los medicos, donde estos mismos estan en una matriz(lista) de diccionarios
    """
    while True:
        print("\n" + "="*40)
        print("[0] , Volver al menu principal") 
        print("[1] , Mostrar lista de medicos ") 
        print("[2] , Agregar medico " )
        print("[3] , Eliminar medico de la lista ")
        print("[4] , Modificar medico")
        print("[5] , Mostrar Historial de un medico")
        print("="*40)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion == 1:
            Medicos.MostrartablaMedicos()
            os.system('cls')
        elif opcion == 2:
            Medicos.agregarMedico()
        elif opcion == 3:
            Medicos.eliminarMedico()
            os.system('cls')
        elif opcion == 4:
            Medicos.modificarMedico()
        elif opcion == 5:
            Medicos.mostrarHistorialMedico()
        elif opcion == 0:
            os.system('cls')
            return
        else: 
            print("Opcion Invalida, Ingrese nuevamente los datos:")
            input("\nPresione Enter para continuar...")


def menuPacientes(): #Menu de los pacientes
    os.system('cls')
    """
    Menu en donde se puede eliminar,agregar o modificar la lista de los pacientes, donde estos mismos estan en una matriz(lista) de diccionarios
    """
    while True:
        print("\n" + "="*40)
        print("[0] , Volver al menu principal") 
        print("[1] , Mostrar lista de pacientes ") 
        print("[2] , Agregar paciente" )
        print("[3] , Eliminar paciente de la lista ")
        print("[4] , Modificar paciente")
        print("="*40)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion == 1:
            Pacientes.mostrarLista()
            os.system('cls')
        elif opcion == 2:
            Pacientes.agregarPaciente()
        elif opcion == 3:
            Pacientes.eliminarPaciente()
        elif opcion == 4:
            Pacientes.modificarPaciente()
        elif opcion == 0:
            os.system('cls')
            return
        else: 
            print("Opcion Invalida, Ingrese nuevamente los datos:")
            input("\nPresione Enter para continuar...")

def menuTurnos():# Menu Turnos
    os.system('cls')
    """
    El paciente puede agendar o cancelar un turno de la lista de medicos
    """
    while True:
        print("\n" + "="*40)
        print("[0] , Volver al menu principal " )
        print("[1] , Agendar Turno") 
        print("[2] , Cancelar Turno ") 
        print("="*40)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion == 1:
            Turnos.agendarTurno()
            os.system('cls')
        elif opcion == 2:
            Turnos.cancelarTurno()
            os.system('cls')
        elif opcion == 0:
            os.system('cls')
            return


def menuHospital(): # Menu principal
    os.system('cls')
    while True:
        print("\n" + "="*40)
        print("[0] , Salir del programa " )
        print("[1] , Mostrar Menu de Medico " )
        print("[2] , Mostrar Menu de Paciente")
        print("[3] , Mostrar Menu de Turno")
        print("="*40)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion == 1:
            menuMedicos()
        elif opcion == 2:
            menuPacientes()
        elif opcion == 3:
            menuTurnos()
        elif opcion == 0:
             os.system('cls')
             return

def main():
    menuHospital()
    os.system('cls')
    print("Saliendo del programa...")
    time.sleep(2)
    sys.exit()
main()