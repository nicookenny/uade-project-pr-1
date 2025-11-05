import Storage
import FuncionesGenerales

def CargarObraSocial():
    #Carga la obra social de un paciente.
    print("=" * 40)
    for obras in Storage.obras_y_prepagas_arg:
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
    for pacienteWithKey in Storage.Pacientes.listar():
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
        paciente_info = Storage.Pacientes.obtener(dni)
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
            if not FuncionesGenerales.confirmar_accion("¿Desea confirmar el alta del paciente?", "Alta cancelada por el usuario."):
                return

            Storage.Pacientes.agregar(newPaciente)
            print(f"El paciente {nombre} se agregó correctamente")
            FuncionesGenerales.pausar()
            break
    mostrarLista()
    FuncionesGenerales.limpiar_pantalla()


def eliminarPaciente():
    while True:
        mostrarLista()
        dni = FuncionesGenerales.CargarDNI("paciente")

        paciente_info = Storage.Pacientes.obtener(dni)
        if not paciente_info:
            print("El paciente no existe en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        _, datos = paciente_info
        nombre = datos["Nombre"]
        visualizarDatos(datos,Encabezado="Datos del paciente a eliminar:")
        if not FuncionesGenerales.confirmar_accion("¿Desea confirmar?", "Eliminación cancelada por el usuario."):
            return

        Storage.Pacientes.eliminar(dni)
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

        paciente_info = Storage.Pacientes.obtener(dni)
        if not paciente_info:
            print("El paciente no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        _, datos = paciente_info

        FechaDeNacimiento = FuncionesGenerales.CargarFechaDeNacimiento()
        nombre = FuncionesGenerales.CargarNombre()
        obrasocial = CargarObraSocial()

        new_data = {
            "Nombre": nombre,
            "Fecha de Nacimiento": FechaDeNacimiento,
            "Obra Social": obrasocial
        }

        # Actualizar datos temporalmente para visualizar
        datos.update(new_data)
        visualizarDatos(datos,Encabezado="Datos del paciente modificados:")
        if not FuncionesGenerales.confirmar_accion("¿Desea confirmar?", "Modificación cancelada por el usuario."):
            return

        Storage.Pacientes.modificar(dni, new_data)
        print("Se han modificado sus datos correctamente\n")
        FuncionesGenerales.pausar()
        mostrarLista()
        FuncionesGenerales.limpiar_pantalla()
        return


def main(): ...


main()
