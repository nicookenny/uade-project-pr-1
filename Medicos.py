import os
import Datos
from datetime import date


def CalculoEdad(fecha):  # Funcion que sirve para calcular la edad
    hoy = date.today()
    año, mes, dia = fecha
    edad = hoy.year - año - ((hoy.month, hoy.day) < (mes, dia))
    return edad


def MostrartablaMedicos():  # Muestra en forma de tabla los medicos
    os.system("clear")
    print(
        f"{'ID':<3} {'Nombre':<20} {'Edad':<12} {'DNI':<10} {'Especialidad':<30} {'Estado':<12} {'Paciente'}"
    )
    print("-" * 102)
    for medico in Datos.medicos:  # Cada vez que quieras llamar a un diccionario o una tupla le Agregas Datos.Nombre de la tupla o diccionario A usar
        for id_medico, datos in medico.items():
            print(
                f"{id_medico:<3} {datos['Nombre']:<20} {CalculoEdad(datos['Fecha de Nacimiento']):<12} {datos['DNI']:<10} {datos['Especialidad']:<30} {datos['Estado']:<12} {datos['Paciente']}"
            )
    input("\nPresione Enter para continuar...")


def CargaEspecialidad():  # Muestra la especialidades que puede elegir el medico
    print("=" * 40)
    for areas in Datos.especialidades_medicas:
        print(areas)
    print("=" * 40)
    especialidad = input("Ingresar la especialidad:")
    while especialidad not in Datos.especialidades_medicas:
        print("Especialidad no encontrada")
        especialidad = input("Ingresar otra especialidad: ")
    return especialidad


def CargarFechaDeNacimiento():
    carga = True
    while carga:
        dia = int(input("Ingrese su dia de nacimiento: "))
        mes = int(input("Ingrese su mes de nacimiento: "))
        año = int(input("Ingrese su año de nacimiento: "))
        fecha = (año, mes, dia)
        edad = CalculoEdad(fecha)
        if 24 <= edad <= 70:
            carga = False
        else:
            print("Fecha invalida")
    return fecha


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


def CargaDeNuevoMedico(
    nombre, dni, FechaDeNacimiento, Especialidad
):  # Carga un diccionario con los datos del medico
    medico = {
        len(Datos.medicos) + 1: {
            "Nombre": nombre,
            "Fecha de Nacimiento": FechaDeNacimiento,
            "DNI": dni,
            "Especialidad": Especialidad,
            "Estado": "Disponible",
            "Paciente": {},
            "Historial": [],
        }
    }
    return medico


def agregarMedico():  # Agrega un medico al diccionario
    os.system("clear")
    while True:
        print("=" * 40)
        MostrartablaMedicos()
        dni = CargarDNI()

        # Buscar si el médico ya existe a traves de lista por compresion
        dnis_medicos = [
            datos["DNI"] for dicc in Datos.medicos for idMedico, datos in dicc.items()
        ]
        if dni in dnis_medicos:
            nombre = [
                datos["Nombre"]
                for dicc in Datos.medicos
                for idMedico, datos in dicc.items()
                if datos["DNI"] == dni
            ][0]
            print(f"El médico {nombre} ya existe")
            input("\nPresione Enter para continuar")
            os.system("cls")

        else:  # Solo se agrega si no existe
            nombre = CargarNombre()
            FechaDeNacimiento = CargarFechaDeNacimiento()
            Especialidad = CargaEspecialidad()
            Datos.medicos.append(
                CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad)
            )  # Manera de guardar las modificaciones en el archivo de datos
            print("El medico se agregó correctamente")
            input("\nPresione Enter para continuar...")
            break

    MostrartablaMedicos()
    os.system("clear")


def eliminarMedico():  # Elimina de la lista al medico
    os.system("clear")
    while True:
        MostrartablaMedicos()
        band = True
        print()
        print("=" * 40)
        dni = (
            CargarDNI()
        )  # Se busca si el medico existe a traves de su DNI a traves un True/False
        for diccionario in Datos.medicos:
            for medico, datos in diccionario.items():
                if dni == datos["DNI"] and datos["Paciente"] == {}:
                    band = False

        if (
            band == False
        ):  # Iteramos para buscar el indice(posicion) del medico para poder eliminarlo de la lista y forzamos que el bucle rompa a traves de un return con el fin de no tener IndexError
            for diccionario in range(len(Datos.medicos)):
                for medico, datos in Datos.medicos[diccionario].items():
                    if dni == datos["DNI"]:
                        del Datos.medicos[diccionario][medico]
                        print(
                            f"El medico {datos['Nombre']} se elimino correctamente de la lista"
                        )
                        input("\nPresione Enter para continuar...")
                        MostrartablaMedicos()
                        return

        else:
            print("El medico no esta en la lista o tiene informacion importante")
            input("\n presione enter para continuar")
            os.system("clear")


def modificarMedico():  # Modifica datos del medico
    os.system("clear")
    while True:
        encontrado = False
        MostrartablaMedicos()
        dni = CargarDNI()
        for diccionario in Datos.medicos:
            for medico, datos in diccionario.items():
                if dni == datos["DNI"] and datos["Paciente"] == {}:
                    encontrado = True
                    # Modificar los datos
                    FechaDeNacimiento = CargarFechaDeNacimiento()
                    nombre = CargarNombre()
                    especialidad = CargaEspecialidad()

                    datos["Nombre"] = nombre
                    datos["Fecha de Nacimiento"] = FechaDeNacimiento
                    datos["Especialidad"] = especialidad

                    print("Se han modificado sus datos correctamente \n")
                    MostrartablaMedicos()
                    os.system("clear")
                    return

        if not encontrado:
            print("El medico no está en la lista o tiene información importante")
            input("\nPresione Enter para continuar")
            os.system("clear")


"""
Esta funcion se encarga de mostrar el historial de los pacientes que se atendieron con un medico, ademas de comparar entre dos medicos sus historiales
"""


def mostrarHistorialMedico():
    os.system("clear")
    while True:
        print("\n" + "=" * 40)
        print("[1] , Mostrar historial de un medico")
        print("[2] , Mostrar historial entre 2 Medicos ")
        opcion = int(
            input("Ingresar una Opcion: ")
        )  # Podes elegir comparar historiales o ver uno solo
        if opcion == 1:
            mostrarHistorialMedico1()
            return

        if opcion == 2:  # Compara entre dos medicos sus historiales
            mostrarHistorialMedico2()
            return


def mostrarHistorialMedico1():
    while True:
        MostrartablaMedicos()
        dni = int(
            input("Ingresar numero de documento del Medico: ")
        )  # Verificamos que el medico existe
        for diccionario in Datos.medicos:
            for medico, dato in diccionario.items():
                if dni == dato["DNI"]:
                    while True:
                        if (
                            len(dato["Historial"]) < 3 and len(dato["Historial"]) >= 1
                        ):  # Si el historial es menor que 3 pacientes lo muestra en pantalla con un print
                            print(f"\n{dato['Historial']}")
                            input("\nPresione Enter para continuar")
                            os.system("cls")
                            return
                        elif (
                            dato["Historial"] == []
                        ):  # Si el historial es una lista vacia que 3 quiere decir que el medico no atendio a ningun paciente
                            print("El medico no tiene historial clinico")
                            input("\nPresione Enter para continuar")
                            os.system("clear")
                            return
                        else:
                            print("\n" + "=" * 40)
                            print("[1] , Mostrar los primeros 6 pacientes")
                            print("[2] , Mostrar todo el historial Medico ")
                            opcio = int(input("Ingresar una Opcion: "))
                            if opcio == 1:
                                ultimosTres = dato[
                                    "Historial"
                                ][
                                    :6
                                ]  # a traves de la tecnica de rebanado mostramos hasta los primeros 6 pacientes
                                print(f"{ultimosTres}")
                                input("\nPresione Enter para continuar")
                                os.system("clear")
                                return
                            elif (
                                opcio == 2
                            ):  # Muestra el historial completo de los pacientes atendidos por el medico
                                print(f"{dato['Historial']}")
                                input("\nPresione Enter para continuar")
                                os.system("clear")
                                return
                            else:
                                print("Opcion incorrecta")
                                input("\nPresione Enter para continuar")
                                os.system("clear")

        print("El medico no esta en la lista")
        input("\nPresione Enter para continuar")
        os.system("clear")


def mostrarHistorialMedico2():
    os.system("clear")
    MostrartablaMedicos()
    while True:
        band = False
        medico1 = int(
            input("Ingresar numero de documento del primer medico elegido: ")
        )  # Verificamos que exista el primer medico
        for diccionario in Datos.medicos:
            for medico, datos in diccionario.items():
                if medico1 == datos["DNI"] and datos["Historial"] != []:
                    auxMedico1 = datos
                    id1 = medico
                    band = True
        if band == True:
            while True:
                band1 = False
                medico2 = int(
                    input("Ingresar numero de documento del segundo medico elegido: ")
                )  # Verificamos que exista el segundo medico
                for diccionario in Datos.medicos:
                    for medic, dato in diccionario.items():
                        if (
                            medico2 == dato["DNI"]
                            and dato["Historial"] != []
                            and dato["DNI"]
                        ):
                            auxMedico2 = dato
                            id2 = medic
                            band1 = True

                if band1 == True:
                    if (
                        auxMedico1 == auxMedico2
                    ):  # Verificamos que no sea el mismo medico el que se compara
                        print("Los medicos son los mismos, eliga otro por favor")
                        input("\nPresione Enter para continuar")
                        return
                    else:
                        os.system("clear")
                        historial1_dict = {}
                        historial2_dict = {}
                        for medico in Datos.medicos:  # Iteramos por la clave del medico y su valor del historial para agregarlo a un diccionario
                            if id1 in medico:
                                for paciente in medico[id1]["Historial"]:
                                    historial1_dict.update(paciente)
                            if id2 in medico:
                                for paciente in medico[id2]["Historial"]:
                                    historial2_dict.update(paciente)

                        """
                        Convertimos a cada diccionario en un conjunto para utilizar operaciones con el fin de comparar cada historial
                        """
                        historialMedico1 = set(historial1_dict.keys())
                        historialMedico2 = set(historial2_dict.keys())

                        comunes = historialMedico1 & historialMedico2
                        exclusivosPrimero = historialMedico1 - historialMedico2
                        exclusivosSegundo = historialMedico2 - historialMedico1

                        print("\nPacientes en comun:")
                        for pacientes in comunes:
                            print(historial1_dict[pacientes])

                        print("\nPacientes exclusivos del primero:")
                        for pacientes in exclusivosPrimero:
                            print(historial1_dict[pacientes])

                        print("\nPacientes exclusivos del segundo:")
                        for pacientes in exclusivosSegundo:
                            print(historial2_dict[pacientes])

                        input("\nPresione Enter para continuar")
                        os.system("clear")
                        return

                else:
                    print(
                        "El medico no esta en la lista o el historial medico esta vacio"
                    )
                    input("\nPresione Enter para continuar")
                    os.system("clear")
                    MostrartablaMedicos()
        else:
            print("El medico no esta en la lista o el historial medico esta vacio")
            input("\nPresione Enter para continuar")
            os.system("clear")
            return


def main(): ...


main()
