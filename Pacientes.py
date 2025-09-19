import os
import Datos
from datetime import date


def limpiar_pantalla():
    os.system(
        "cls" if os.name == "nt" else "clear"
    )  # cls es solo para windows, clear es para linux y mac


def pausar():
    """
    Pausa la ejecución del programa y espera a que el usuario presione Enter para continuar.
    """
    input("\nPresione Enter para continuar...")


def CalculoEdad(fecha):
    """
    Calcula la edad de una persona a partir de su fecha de nacimiento.
    """
    hoy = date.today()
    año, mes, dia = fecha
    edad = hoy.year - año - ((hoy.month, hoy.day) < (mes, dia))
    return edad


def buscar_paciente(dni):
    for i, paciente in enumerate(Datos.pacientes):
        if paciente["DNI"] == dni:
            return (i, paciente)
    return None


def paciente_existe(dni):
    return buscar_paciente(dni) is not None


def CargarDNI():
    dni = input("Ingresar número de documento: ")
    while not dni.isdigit() or len(dni) != 8:
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
    """
    Carga la obra social de un paciente.
    """

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


def CargaDeNuevoPaciente(nombre, dni, FechaDeNacimiento, ObraSocial):
    return {
        dni: {
            "Nombre": nombre,
            "Fecha de Nacimiento": FechaDeNacimiento,
            "Obra Social": ObraSocial,
        }
    }


def mostrarLista():
    limpiar_pantalla()
    print(f"{'DNI':<8} {'Nombre':<20} {'Edad':<12} {'Obra Social'}")
    print("-" * 102)
    for paciente in Datos.pacientes:
        print(
            f"{paciente['DNI']:<8} {paciente['Nombre']:<20} {CalculoEdad(paciente['Fecha de Nacimiento']):<12} {paciente['Obra Social']}"
        )
    pausar()


def agregarPaciente():
    limpiar_pantalla()
    while True:
        print("=" * 40)
        mostrarLista()
        dni = CargarDNI()

        paciente_info = buscar_paciente(dni)
        if paciente_info:
            print(f"El paciente {paciente_info[1]['Nombre']} ya existe")
            pausar()
            limpiar_pantalla()
        else:
            nombre = CargarNombre()
            FechaDeNacimiento = CargarFechaDeNacimiento()
            obrasocial = CargarObraSocial()
            Datos.pacientes.append(
                CargaDeNuevoPaciente(nombre, dni, FechaDeNacimiento, obrasocial)
            )
            print("El paciente se agregó correctamente")
            pausar()
            break
    mostrarLista()
    limpiar_pantalla()


def eliminarPaciente():
    while True:
        mostrarLista()
        dni = CargarDNI()

        paciente_info = buscar_paciente(dni)
        if not paciente_info:
            print("El paciente no existe en la lista")
            pausar()
            limpiar_pantalla()
            continue

        idx, datos = paciente_info
        nombre = datos["Nombre"]

        del Datos.pacientes[idx]
        print(f"El paciente {nombre} se elimino correctamente de la lista")
        pausar()
        mostrarLista()
        limpiar_pantalla()
        return


def modificarPaciente():
    limpiar_pantalla()
    while True:
        mostrarLista()
        dni = CargarDNI()

        paciente_info = buscar_paciente(dni)
        if not paciente_info:
            print("El paciente no esta en la lista")
            pausar()
            limpiar_pantalla()
            continue

        _, datos = paciente_info

        FechaDeNacimiento = CargarFechaDeNacimiento()
        nombre = CargarNombre()
        obrasocial = CargarObraSocial()

        datos["Nombre"] = nombre
        datos["Fecha de Nacimiento"] = FechaDeNacimiento
        datos["Obra Social"] = obrasocial

        print("Se han modificado sus datos correctamente\n")
        pausar()
        mostrarLista()
        limpiar_pantalla()
        return


def main(): ...


main()
