import Datos
import FuncionesGenerales

def buscar_paciente(dni):
    for i, paciente in enumerate(Datos.pacientes):
        if paciente["DNI"] == dni:
            return (i, paciente)
    return None

def paciente_existe(dni):
    return buscar_paciente(dni) is not None

def CargarObraSocial():
    #Carga la obra social de un paciente.
    print("=" * 40)
    for obras in Datos.obras_y_prepagas_arg:
        print(obras)
    print("=" * 40)
    obrasocial = input("Ingresar la Obra Social: ")
    while obrasocial == "" or obrasocial.isnumeric():
        print("Obra Social no válida")
        obrasocial = input("Intente nuevamente: ")
    return obrasocial

def CargaDeNuevoPaciente(nombre, dni, FechaDeNacimiento, ObraSocial):
    return {
        "DNI": dni,
        "Nombre": nombre,
        "Fecha de Nacimiento": FechaDeNacimiento,
        "Obra Social": ObraSocial,
    }

def mostrarLista():
    FuncionesGenerales.limpiar_pantalla()
    print(f"{'DNI':<8} {'Nombre':<20} {'Edad':<12} {'Obra Social'}")
    print("-" * 102)
    for pacienteWithKey in Datos.pacientes:
        print(
            f"{pacienteWithKey['DNI']:<8} {pacienteWithKey['Nombre']:<20} {FuncionesGenerales.CalculoEdad(pacienteWithKey['Fecha de Nacimiento']):<12} {pacienteWithKey['Obra Social']}"
        )
    FuncionesGenerales.pausar()

def visualizarDatos(lista,Encabezado):  
    FuncionesGenerales.limpiar_pantalla()
    print("=" * 40)
    print(f"{Encabezado}")
    print(f"Nombre completo: {lista['Nombre']}")
    print(f"Fecha de Nacimiento: {lista['Fecha de Nacimiento'][2]}/{lista['Fecha de Nacimiento'][1]}/{lista['Fecha de Nacimiento'][0]}")
    print(f"Edad:{FuncionesGenerales.CalculoEdad(lista['Fecha de Nacimiento'])} años")
    print(f"DNI: {lista['DNI']}")
    print(f"Obra social:{lista['Obra Social']}")
    print("=" * 40)

def agregarPaciente():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        print("=" * 40)
        mostrarLista()
        dni = FuncionesGenerales.CargarDNI("paciente")
        paciente_info = buscar_paciente(dni)
        if paciente_info:
            print(f"El paciente {paciente_info[1]['Nombre']} ya existe")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
        else:
            nombre = FuncionesGenerales.CargarNombre()
            FechaDeNacimiento = FuncionesGenerales.CargarFechaDeNacimiento()
            obrasocial = CargarObraSocial()
            newPaciente=CargaDeNuevoPaciente(nombre, dni, FechaDeNacimiento, obrasocial)
            visualizarDatos(newPaciente,Encabezado="Resumen de datos del nuevo paciente:")
            confirmar = input("\n¿Desea confirmar el alta del paciente? (s/n): ").lower()
            if confirmar != "s":
                print("Alta cancelada por el usuario.")
                FuncionesGenerales.pausar()
                FuncionesGenerales.limpiar_pantalla()
                return
            
            Datos.pacientes.append(newPaciente)
            print(f"El paciente {nombre} se agregó correctamente")
            FuncionesGenerales.pausar()
            break
    mostrarLista()
    FuncionesGenerales.limpiar_pantalla()


def eliminarPaciente():
    while True:
        mostrarLista()
        dni = FuncionesGenerales.CargarDNI("paciente")

        paciente_info = buscar_paciente(dni)
        if not paciente_info:
            print("El paciente no existe en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        idx, datos = paciente_info
        nombre = datos["Nombre"]
        visualizarDatos(datos,Encabezado="Datos del paciente a eliminar:")
        confirmar = input("\n¿Desea confirmar? (s/n): ").lower()
        if confirmar != "s":
            print("Modificación cancelada por el usuario.")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return
        
        del Datos.pacientes[idx]
        print(f"El paciente {nombre} se elimino correctamente de la lista")
        FuncionesGenerales.pausar()
        mostrarLista()
        FuncionesGenerales.limpiar_pantalla()
        return


def modificarPaciente():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        mostrarLista()
        dni = FuncionesGenerales.CargarDNI("paciente")

        paciente_info = buscar_paciente(dni)
        if not paciente_info:
            print("El paciente no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        _, datos = paciente_info

        FechaDeNacimiento = FuncionesGenerales.CargarFechaDeNacimiento()
        nombre = FuncionesGenerales.CargarNombre()
        obrasocial = CargarObraSocial()

        datos["Nombre"] = nombre
        datos["Fecha de Nacimiento"] = FechaDeNacimiento
        datos["Obra Social"] = obrasocial
        visualizarDatos(datos,Encabezado="Datos del paciente modificados:")
        confirmar = input("\n¿Desea confirmar? (s/n): ").lower()
        if confirmar != "s":
            print("Modificación cancelada por el usuario.")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            return
        
        print("Se han modificado sus datos correctamente\n")
        FuncionesGenerales.pausar()
        mostrarLista()
        FuncionesGenerales.limpiar_pantalla()
        return


def main(): ...


main()
