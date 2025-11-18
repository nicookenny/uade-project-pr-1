import gestor_datos
import FuncionesGenerales

def CargarObraSocial():
    print("=" * 40)
    print("Seleccione una Obra Social:")
    for i, obra in enumerate(gestor_datos.obras_y_prepagas_arg, 1):
        print(f"[{i}] {obra}")
    print("=" * 40)

    while True:
        try:
            opcion = int(input("Ingrese el número de la Obra Social: "))
            if 1 <= opcion <= len(gestor_datos.obras_y_prepagas_arg):
                return gestor_datos.obras_y_prepagas_arg[opcion - 1]
            print(f"Opción inválida. Debe estar entre 1 y {len(gestor_datos.obras_y_prepagas_arg)}")
        except ValueError:
            print("Debe ingresar un número")

def CargaDeNuevoPaciente(nombre, dni, FechaDeNacimiento, ObraSocial):
    return {
        "DNI": dni,
        "Nombre": nombre,
        "Fecha de Nacimiento": FechaDeNacimiento,
        "Obra Social": ObraSocial,
    }

def mostrarLista():
    FuncionesGenerales.limpiar_pantalla()
    ancho_tabla = 102
    titulo = "LISTADO DE PACIENTES"
  
    print("=" * ancho_tabla)
    print(titulo.center(ancho_tabla))
    print("=" * ancho_tabla)
    
    print(f"{'DNI':<12} {'Nombre':<25} {'Edad':<8} {'Obra Social':<57}")
    print("-" * ancho_tabla)
    
    lista_pacientes = gestor_datos.datos["pacientes"]
    
    if not lista_pacientes:
        print("No hay pacientes registrados.".center(ancho_tabla))

    for paciente in lista_pacientes:
        edad = FuncionesGenerales.CalculoEdad(paciente['Fecha de Nacimiento'])
        print(
            f"{paciente['DNI']:<12} {paciente['Nombre']:<25} {edad:<8} {paciente['Obra Social']:<57}"
        )
    
    print("=" * ancho_tabla)
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
        dni = FuncionesGenerales.CargarDNI("paciente que quiere agregar")
        paciente_info = gestor_datos.obtener_paciente(dni)
        if paciente_info:
            print(f"El paciente {paciente_info['Nombre']} ya existe")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
        else:
            nombre = FuncionesGenerales.CargarNombre()
            FechaDeNacimiento = FuncionesGenerales.CargarFechaDeNacimiento()
            FuncionesGenerales.limpiar_pantalla()
            obrasocial = CargarObraSocial()
            newPaciente=CargaDeNuevoPaciente(nombre, dni, FechaDeNacimiento, obrasocial)
            visualizarDatos(newPaciente,Encabezado="Resumen de datos del nuevo paciente:")
            if not FuncionesGenerales.confirmar_accion("¿Desea confirmar el alta del paciente?", "Alta cancelada por el usuario."):
                return

            gestor_datos.agregar_paciente(newPaciente)
            print(f"El paciente {nombre} se agregó correctamente")
            FuncionesGenerales.pausar()
            break
    mostrarLista()
    FuncionesGenerales.limpiar_pantalla()


def eliminarPaciente():
    while True:
        mostrarLista()
        dni = FuncionesGenerales.CargarDNI("paciente que quiere eliminar")

        paciente_info = gestor_datos.obtener_paciente(dni)
        if not paciente_info:
            print("El paciente no existe en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        datos = paciente_info
        nombre = datos["Nombre"]
        visualizarDatos(datos,Encabezado="Datos del paciente a eliminar:")
        if not FuncionesGenerales.confirmar_accion("¿Desea confirmar?", "Eliminación cancelada por el usuario."):
            return

        gestor_datos.eliminar_paciente(dni)
        print(f"El paciente {nombre} se elimino correctamente de la lista")
        FuncionesGenerales.pausar()
        mostrarLista()
        FuncionesGenerales.limpiar_pantalla()
        return


def modificarPaciente():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        mostrarLista()
        dni = FuncionesGenerales.CargarDNI("paciente que quiere modificar")

        paciente_info = gestor_datos.obtener_paciente(dni)
        if not paciente_info:
            print("El paciente no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        datos = paciente_info

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

        gestor_datos.modificar_paciente(dni, new_data)
        print("Se han modificado sus datos correctamente\n")
        FuncionesGenerales.pausar()
        mostrarLista()
        FuncionesGenerales.limpiar_pantalla()
        return


def buscarPaciente():
    paciente = FuncionesGenerales.buscar_persona(gestor_datos.listar_pacientes(), tipo_busqueda="ambos")
    if paciente:
        visualizarDatos(paciente, Encabezado="Datos del paciente encontrado:")
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return paciente
    return None

def main(): ...


main()
