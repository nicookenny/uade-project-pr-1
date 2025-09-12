import os
from menues import doctors_menu, main_menu


medicos = []


def showMenu(options: dict[str, str]):
    print("\n" + "=" * 40)
    for key, value in options.items():
        print(f"[{key}] {value['text']}")
    print("=" * 40)


def mostrarLista(medicos):
    for medico in medicos:
        for med, datos in medico.items():
            print("\n")
            print(med, datos)
    return


def agregarMedico(medico):  # Agrega un medico al diccionario
    while True:
        for medic in medico:
            for med, datos in medic.items():
                print("\n")
                print(med, datos)
        band = True
        print()
        print("=" * 40)
        dni = int(
            input("Ingresar numero de documento: ")
        )  # Se busca si el medico existe a traves de su DNI a traves un True/False
        for diccionario in medico:
            for medicos, datos in diccionario.items():
                if dni == datos["DNI"][0]:
                    band = False
                    break

        if band == True:  # Se ingresa los datos del medico a agregar
            medico.append(
                {
                    "Medico_" + str(len(medico) + 1): {
                        "Nombre": input("ingresar el nombre: "),
                        "Edad": input("ingresar edad: "),
                        "DNI": (dni,),
                        "Especialidad": input("ingresar especialidad: "),
                    }
                }
            )
            print("El medico se agrego correctamente")
            input("\nPresione Enter para continuar...")

            break

        else:
            print("El medico ya existe")
            input("\n presione enter para continuar")
            os.system("clear")

    return


def eliminarMedico(medico):  # Elimina de la lista al medico
    while True:
        for medic in medico:
            for med, datos in medic.items():
                print("\n")
                print(med, datos)
        band = True
        print()
        print("=" * 40)
        dni = int(
            input("Ingresar numero de documento: ")
        )  # Se busca si el medico existe a traves de su DNI a traves un True/False
        for diccionario in medico:
            for medicos, datos in diccionario.items():
                if dni == datos["DNI"][0]:
                    band = False
                    break

        if (
            band == False
        ):  # Iteramos para buscar el indice(posicion) del medico para poder eliminarlo de la lista y forzamos que el bucle rompa a traves de un return con el fin de no tener IndexError
            print(band)
            for diccionario in range(len(medico)):
                for medicos, datos in medico[diccionario].items():
                    if dni == datos["DNI"][0]:
                        print(band)
                        del medico[diccionario]
                        print(
                            f"El {medicos}, {datos['Nombre']} se elimino correctamente de la lista"
                        )
                        input("\nPresione Enter para continuar...")
                        return

        else:
            print("El medico no esta en la lista")
            input("\n presione enter para continuar")
            os.system("clear")


def modificarMedico(medico):  # Modifica datos del medico
    while True:
        for medic in medico:
            for med, datos in medic.items():
                print("\n")
                print(med, datos)
        print()
        print("=" * 40)
        dni = int(input("Ingresar DNI del medico: "))

        for diccionario in (
            medico
        ):  # Verificamos que existe y una vez encontrado se modifican sus datos
            for medicos, datos in diccionario.items():
                if dni == datos["DNI"][0]:
                    while True:
                        edad = int(input("Ingresar edad: "))
                        if edad < 20:
                            print("La edad no es suficiente")
                        else:
                            nombre = input("Ingresar Nombre: ")
                            especialidad = input("Ingresar la especialidad: ")
                            datos["Nombre"] = nombre
                            datos["Edad"] = str(edad)
                            datos["Especialidad"] = especialidad
                            print(
                                f"El {medicos} se han modificado sus datos correctamente"
                            )
                            input("\n presione enter para continuar")
                            return

        print("El medico no esta en la lista")
        input("\n presione enter para continuar")
        os.system("clear")


def menuMedicos():  # Menu de los medicos
    os.system("clear")
    """
    Menu en donde se puede eliminar,agregar o modificar la lista de los medicos, donde estos mismos estan en una matriz(lista) de diccionarios
    """
    medicos = [
        {
            "Medico_1": {
                "Nombre": "Gonzalez Juan",
                "Edad": "30",
                "DNI": (48120054,),
                "Especialidad": "Traumatologo",
                "Estado": "Disponible",
            }
        },
        {
            "Medico_2": {
                "Nombre": "Ortiz Mariana",
                "Edad": "26",
                "DNI": (45063213,),
                "Especialidad": "Pediatra",
            }
        },
        {
            "Medico_3": {
                "Nombre": "Lopez Esteban",
                "Edad": "37",
                "DNI": (43170055,),
                "Especialidad": "Oculista",
            }
        },
    ]

    while True:
        showMenu(doctors_menu)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion in doctors_menu:
            doctors_menu[opcion]["action"]()
        else:
            print("Opcion Invalida, Ingrese nuevamente los datos:")
            input("\nPresione Enter para continuar...")


def menuHospital():  # Menu principal
    os.system("clear")
    while True:
        showMenu(main_menu)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion in main_menu:
            main_menu[opcion]["action"]()
        else:
            return


def main():
    menuHospital()
    os.system("clear")
    print("Saliendo del programa...")


main()
