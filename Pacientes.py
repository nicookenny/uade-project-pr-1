import os
from Datos import pacientes
import Datos
from datetime import date


def CalculoEdad(fecha):
    hoy = date.today()
    año, mes, dia = fecha
    edad = hoy.year - año - ((hoy.month, hoy.day) < (mes, dia))
    return edad


def CargarDNI():
    dni = input("Ingresar número de documento: ")
    while not dni.isdigit() or len(dni) != 8 or not dni:
        print("DNI inválido")
        dni = input("Ingresar otro número de documento: ")
    return int(dni)


def CargarNombre():
    nombre = input("Ingresar el nombre: ")
    while nombre == "" or nombre.isnumeric():
        print("Nombre no válido")
        nombre = input("Ingrese otro nombre: ")
    return nombre


def CargarObraSocial():
    print("=" * 40)
    for obras in Datos.obras_y_prepagas_arg:
        print(obras)
    print("=" * 40)
    obrasocial = input("Ingresar la Obra Social: ")
    while obrasocial == "" or obrasocial.isnumeric():
        print("Obra Social no válida")
        obrasocial = input("Intente nuevamente: ")
    return obrasocial


def CargarFechaDeNacimiento():
    carga = True
    while carga:
        dia = int(input("Ingrese su dia de nacimiento: "))
        mes = int(input("Ingrese su mes de nacimiento: "))
        año = int(input("Ingrese su año de nacimiento: "))
        fecha = (año, mes, dia)
        edad = CalculoEdad(fecha)
        if edad > 0:
            carga = False
        else:
            print("Fecha invalida")
    return fecha


def CargaDeNuevPaciente(nombre, dni, FechaDeNacimiento, ObraSocial):
    paciente = {
        dni: {
            "Nombre": nombre,
            "Fecha de Nacimiento": FechaDeNacimiento,
            "Obra Social": ObraSocial,
        }
    }
    return paciente


def mostrarLista():
    os.system("clear")
    print(f"{'ID':<8} {'Nombre':<20} {'Edad':<12} {'Obra Social'} ")
    print("-" * 102)
    for paciente in Datos.pacientes:  # Cada vez que quieras llamar a un diccionario o una tupla le Agregas Datos.Nombre de la tupla o diccionario A usar
        for id_paciente, datos in paciente.items():
            print(
                f"{id_paciente:<8} {datos['Nombre']:<20} {CalculoEdad(datos['Fecha de Nacimiento']):<12} {datos['Obra Social']} "
            )
    input("\nPresione Enter para continuar...")
    return


def agregarPaciente():
    os.system("cls")
    while True:
        print("=" * 40)
        mostrarLista()
        dni = CargarDNI()

        # Verifica si el paciente existe
        dnisPacientes = [
            idPaciente for dicc in Datos.pacientes for idPaciente, datos in dicc.items()
        ]
        if dni in dnisPacientes:
            nombre = [
                datos["Nombre"]
                for dicc in Datos.pacientes
                for idPaciente, datos in dicc.items()
                if idPaciente == dni
            ]
            print(f"El paciente {nombre} ya existe")
            input("\nPresione Enter para continuar")
            os.system("clear")

        else:
            nombre = CargarNombre()
            FechaDeNacimiento = CargarFechaDeNacimiento()
            obrasocial = CargarObraSocial()
            Datos.pacientes.append(
                CargaDeNuevPaciente(nombre, dni, FechaDeNacimiento, obrasocial)
            )
            print("El paciente se agregó correctamente")
            input("\nPresione Enter para continuar...")
            break
    mostrarLista()
    os.system("cls")


def eliminarPaciente():
    while True:
        mostrarLista()
        existeDni = True
        dni = CargarDNI()
        for diccionario in pacientes:
            for identificacion, datos in diccionario.items():
                if dni == identificacion:
                    existeDni = False

        if existeDni == False:
            for diccionario in range(len(pacientes)):
                for identificacion, datos in pacientes[diccionario].items():
                    if dni == identificacion:
                        del pacientes[diccionario]
                        print(
                            f"El paciente {datos['Nombre']} se elimino correctamente de la lista"
                        )
                        input("\nPresione Enter para continuar")
                        mostrarLista()
                        os.system("clear")
                        return

        print("El paciente no existe en la lista")
        input("\nPresione Enter para continuar")
        os.system("clear")


def modificarPaciente():
    os.system("cls")
    while True:
        PacienteEncontrado = False
        mostrarLista()
        dni = CargarDNI()
        for diccionario in Datos.pacientes:
            for paciente, datos in diccionario.items():
                if dni == paciente:
                    PacienteEncontrado = True

                    # modificar los datos
                    FechaDeNacimiento = CargarFechaDeNacimiento()
                    nombre = CargarNombre()
                    obrasocial = CargarObraSocial()

                    datos["Nombre"] = nombre
                    datos["Fecha de Nacimiento"] = FechaDeNacimiento
                    datos["Obra Social"] = obrasocial

                    print("Se han modificado sus datos correctamente \n")
                    input("\n Presione Enter para continuar")
                    mostrarLista()
                    os.system("cls")
                    return

        if not PacienteEncontrado:
            print("El paciente no esta en la lista")
            input("\n Presione Enter para continuar")
            os.system("cls")


def main(): ...


main()
