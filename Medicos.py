import FuncionesGenerales
import gestor_datos
from datetime import date
from functools import reduce


def mostrar_historial(historial):
    for hist_entry in historial:
        resultado = gestor_datos.obtener_paciente(hist_entry["paciente_dni"])
        paciente = resultado if resultado else None
        if paciente:
            print(f"DNI: {paciente['DNI']}")
            print(f"  Nombre: {paciente['Nombre']}")
            print(
                f"  Fecha de Nacimiento: {paciente['Fecha de Nacimiento'][2]:02d}/{paciente['Fecha de Nacimiento'][1]:02d}/{paciente['Fecha de Nacimiento'][0]}"
            )
            print(f"  Obra Social: {paciente['Obra Social']}")
            print(
                f"  Fecha Turno: {hist_entry['fecha'][2]:02d}/{hist_entry['fecha'][1]:02d}/{hist_entry['fecha'][0]}"
            )
            print(f"  Estado: {hist_entry['estado']}")
        else:
            print(f"[ADVERTENCIA] Paciente con DNI {hist_entry['paciente_dni']} no encontrado en la base de datos")
        print("-" * 30)


def mostrar_historial_paginado(historial, cantidad=6):
    total = len(historial)
    inicio = 0
    while inicio < total:
        print("-" * 30)
        fin = min(inicio + cantidad, total)
        for hist_entry in historial[inicio:fin]:
            resultado = gestor_datos.obtener_paciente(hist_entry["paciente_dni"])
            paciente = resultado if resultado else None
            if paciente:
                print(f"DNI: {paciente['DNI']}")
                print(f"  Nombre: {paciente['Nombre']}")
                print(
                    f"  Fecha de Nacimiento: {paciente['Fecha de Nacimiento'][2]:02d}/{paciente['Fecha de Nacimiento'][1]:02d}/{paciente['Fecha de Nacimiento'][0]}"
                )
                print(f"  Obra Social: {paciente['Obra Social']}")
                print(
                    f"  Fecha Turno: {hist_entry['fecha'][2]:02d}/{hist_entry['fecha'][1]:02d}/{hist_entry['fecha'][0]}"
                )
                print(f"  Estado: {hist_entry['estado']}")
            else:
                print(f"[ADVERTENCIA] Paciente con DNI {hist_entry['paciente_dni']} no encontrado en la base de datos")
            print("-" * 30)
        inicio += cantidad
        if inicio < total:
            if not FuncionesGenerales.confirmar_accion(
                "¿Desea ver más historiales?", ""
            ):
                break

def visualizarDatos(lista, Encabezado):
    FuncionesGenerales.limpiar_pantalla()
    print("=" * 40)
    print(f"{Encabezado}")
    print(f"Nombre completo: {lista['Nombre']}")
    print(
        f"Fecha de Nacimiento: {lista['Fecha de Nacimiento'][2]}/{lista['Fecha de Nacimiento'][1]}/{lista['Fecha de Nacimiento'][0]}"
    )
    print(f"Edad:{FuncionesGenerales.CalculoEdad(lista['Fecha de Nacimiento'])} años")
    print(f"DNI: {lista['DNI']}")
    print(f"Especialidad: {lista['Especialidad']}")
    if "Horarios" in lista:
        print("Horarios de atención:")
        for dia, horario in lista["Horarios"].items():
            if horario:
                print(f"  {dia}: {horario[0]}:00 - {horario[1]}:00")
            else:
                print(f"  {dia}: No disponible")
    else:
        print(f"Estado: {lista['Estado']}")
    print("=" * 40)


def MostrartablaMedicos():
    FuncionesGenerales.limpiar_pantalla()
    ancho_tabla = 100  
    titulo = "TABLA DE MÉDICOS"
 
    print("=" * ancho_tabla)
    print(titulo.center(ancho_tabla))
    print("=" * ancho_tabla)
    
    encabezados = f"{'ID':<5} {'Nombre':<20} {'Edad':<8} {'DNI':<12} {'Especialidad':<40} {'Turnos Hoy':<15}"

    
    print(encabezados)
    print("-" * ancho_tabla)
    
    for i, medico in enumerate(gestor_datos.datos["medicos"], 1):
        hoy = date.today()
        fecha_hoy = (hoy.year, hoy.month, hoy.day)
        turnos_hoy = len(
            [
                t
                for t in gestor_datos.datos["turnos"]
                if t["medico_dni"] == medico["DNI"]
                and t["fecha"] == fecha_hoy
                and t["estado"] == "Confirmado"
            ]
        )
        edad = FuncionesGenerales.CalculoEdad(medico['Fecha de Nacimiento'])
        
        print(
            f"{i:<5} {medico['Nombre']:<20} {edad:<8} {medico['DNI']:<12} {medico['Especialidad']:<40} {turnos_hoy:<15}"
        )
    
    print("=" * ancho_tabla)
    FuncionesGenerales.pausar()


def medico_existe(dni):
    return gestor_datos.obtener_medico(dni) is not None

def CargaEspecialidad():
    print("=" * 40)
    print("Seleccione una especialidad:")
    for i, especialidad in enumerate(gestor_datos.especialidades_medicas, 1):
        print(f"[{i}] {especialidad}")
    print("=" * 40)

    while True:
        try:
            opcion = int(input("Ingrese el número de la especialidad: "))
            if 1 <= opcion <= len(gestor_datos.especialidades_medicas):
                return gestor_datos.especialidades_medicas[opcion - 1]
            print(
                f"Opción inválida. Debe estar entre 1 y {len(gestor_datos.especialidades_medicas)}"
            )
        except ValueError:
            print("Debe ingresar un número")


def CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad):
    return {
        "Nombre": nombre,
        "Fecha de Nacimiento": FechaDeNacimiento,
        "DNI": dni,
        "Especialidad": Especialidad,
        "Estado": "Disponible",
        "Horarios": {
            "Lunes": (9, 18),
            "Martes": (9, 18),
            "Miércoles": (9, 18),
            "Jueves": (9, 18),
            "Viernes": (9, 18),
            "Sábado": None,
            "Domingo": None,
        },
    }


def CargaDeNuevoPacienteDesdemedico(nombre, dni, FechaDeNacimiento):
    """Crea un paciente a partir de los datos del médico con obra social 'Hospital'"""
    return {
        "Nombre": nombre,
        "Fecha de Nacimiento": FechaDeNacimiento,
        "DNI": dni,
        "Obra Social": "Hospital",
    }


"""
Opción 2 (menu)
"""

def agregarMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        #print("=" * 40)
        MostrartablaMedicos()
        dni = FuncionesGenerales.CargarDNI("medico que quieres agregar")

        existe = medico_existe(dni)

        if existe:
            medicoExistente = gestor_datos.obtener_medico(dni)
            print(f"El médico {medicoExistente['Nombre']} ya existe")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
        else:
            nombre = FuncionesGenerales.CargarNombre()
            FechaDeNacimiento = fechaDeNacimientoMedico()
            FuncionesGenerales.limpiar_pantalla()
            Especialidad = CargaEspecialidad()
            newMedico = CargaDeNuevoMedico(nombre, dni, FechaDeNacimiento, Especialidad)
            visualizarDatos(newMedico, Encabezado="Resumen de datos del nuevo médico:")
            if not FuncionesGenerales.confirmar_accion(
                "¿Desea confirmar el alta del médico?", "Alta cancelada por el usuario."
            ):
                return

            # Agregar el médico
            gestor_datos.agregar_medico(newMedico)
            
            # Agregar el médico como paciente también
            newPaciente = CargaDeNuevoPacienteDesdemedico(nombre, dni, FechaDeNacimiento)
            gestor_datos.agregar_paciente(newPaciente)
            
            print(f"El medico {nombre} se agregó correctamente")
            print(f"El medico también fue registrado como paciente con obra social 'Hospital'")
            FuncionesGenerales.pausar()
            break

    MostrartablaMedicos()
    FuncionesGenerales.limpiar_pantalla()

"""
Opción 3 (menu)
"""
def eliminarMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        MostrartablaMedicos()
        print()
        print("=" * 40)
        dni = FuncionesGenerales.CargarDNI("medico que quieres eliminar")

        existe = medico_existe(dni)
        if not existe:
            print("El medico no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        medicoExistente = gestor_datos.obtener_medico(dni)
        nombre_medico = medicoExistente["Nombre"]
        visualizarDatos(medicoExistente, Encabezado="Datos del medico a eliminar:")
        if not FuncionesGenerales.confirmar_accion(
            "¿Desea confirmar?", "Eliminación cancelada por el usuario."
        ):
            return
        gestor_datos.eliminar_medico(dni)
        # También eliminar al médico como paciente
        gestor_datos.eliminar_paciente(dni)
        print(f"El medico {nombre_medico} se elimino correctamente de la lista")
        print(f"El registro del médico como paciente también fue eliminado")
        FuncionesGenerales.pausar()
        MostrartablaMedicos()
        return

"""
Opción 4 (menu)
"""
def modificarMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        MostrartablaMedicos()
        dni = FuncionesGenerales.CargarDNI("medico que quiere eliminar")

        existe = medico_existe(dni)
        if not existe:
            print("El medico no está en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        medicoExistente = gestor_datos.obtener_medico(dni)
        FechaDeNacimiento = fechaDeNacimientoMedico()
        nombre = FuncionesGenerales.CargarNombre()
        especialidad = CargaEspecialidad()

        new_data = {
            "Nombre": nombre,
            "Fecha de Nacimiento": FechaDeNacimiento,
            "Especialidad": especialidad,
        }

        medico_preview = medicoExistente.copy()
        medico_preview.update(new_data)
        visualizarDatos(medico_preview, Encabezado="Datos del medico modificados:")
        if not FuncionesGenerales.confirmar_accion(
            "¿Desea confirmar?", "Modificación cancelada por el usuario."
        ):
            return

        gestor_datos.modificar_medico(dni, new_data)
        print("Se han modificado sus datos correctamente\n")
        MostrartablaMedicos()
        FuncionesGenerales.limpiar_pantalla()
        return
    
"""
Opción 5 (menu)
"""
def mostrarHistorialMedico():
    FuncionesGenerales.limpiar_pantalla()
    ancho_menu = 50
    
    while True:
        print("\n" + "=" * ancho_menu)
        print(" MÓDULO DE HISTORIALES ".center(ancho_menu, "="))
        print("=" * ancho_menu)
        print("\nSeleccione una operación:")
        print("[1] Ver historial de un médico")
        print("[2] Comparar historial entre dos médicos")
        print("\n[Cualquier otra tecla] Volver al menú principal")
        
        opcion = input("Ingresar una Opcion: ").strip()

        if opcion == "1":
            mostrarHistorialMedico1()
            FuncionesGenerales.limpiar_pantalla()
            
        elif opcion == "2":
            mostrarHistorialMedico2()
            FuncionesGenerales.limpiar_pantalla()
            
        else:
            return

def mostrar_opciones_historial(historial):

    if not historial:
        print("\n[INFO] El médico seleccionado no tiene historial clínico.")
        FuncionesGenerales.pausar()
        return True

    if len(historial) <= 6:
        print("\nMostrando el historial completo (6 o menos entradas):")
        mostrar_historial(historial) #
        FuncionesGenerales.pausar()
        return True 

    ancho_menu = 40
    print("\n" + "=" * ancho_menu)
    print(" Opciones de Visualización ".center(ancho_menu, "="))
    print(f"El médico tiene {len(historial)} entradas de historial.")
    print("[1] Mostrar de forma paginada (6 en 6)")
    print("[2] Mostrar historial completo")
    
    try:
        opcion = int(input("Ingresar una Opcion: "))
    except ValueError:
        opcion = 0 

    if opcion == 1:
        mostrar_historial_paginado(historial) 
    elif opcion == 2:
        mostrar_historial(historial)
    else:
        print("Opción incorrecta, volviendo.")

    FuncionesGenerales.pausar()
    return True


def mostrarHistorialMedico1():
    """
    (Sub-menú 1) Muestra el historial de un solo médico.
    """
    ancho_titulo = 50
    FuncionesGenerales.limpiar_pantalla()
    
    # --- ENCABEZADO MEJORADO ---
    print("=" * ancho_titulo)
    print(" Ver Historial de un Médico ".center(ancho_titulo, "="))
    print("=" * ancho_titulo)
    print("\nPrimero, seleccione el médico de la lista:")
    FuncionesGenerales.pausar()

    while True:
        MostrartablaMedicos()
        print("--- Ver Historial de un Médico ---")
        try:
            # (Es mejor si usas tu FuncionesGenerales.CargarDNI aquí)
            dni_input = input("Ingresar DNI del Médico (o 's' para volver): ")
            if dni_input.lower() == 's':
                return
            dni = int(dni_input)
        except ValueError:
            print("Error: DNI debe ser un número.")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        existe = medico_existe(dni)
        if not existe:
            print("El medico no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        historial_medico = gestor_datos.obtener_historial_por_medico(dni)
        
        if mostrar_opciones_historial(historial_medico):
            return


def mostrarHistorialMedico2():
    """
    (Sub-menú 2) Compara el historial de dos médicos.
    """
    ancho_titulo = 50
    FuncionesGenerales.limpiar_pantalla()
    
    print("=" * ancho_titulo)
    print(" Comparar Historiales (2 Médicos) ".center(ancho_titulo, "="))
    print("=" * ancho_titulo)
    
    # --- Pedir PRIMER MÉDICO ---
    print("\nPASO 1: Seleccione al PRIMER médico de la lista:")
    FuncionesGenerales.pausar()
    MostrartablaMedicos()
    
    medico1_dni = None
    while medico1_dni is None:
        try:
            dni_input = input("Ingresar DNI del PRIMER Médico (o 's' para volver): ")
            if dni_input.lower() == 's': return
            dni_temp = int(dni_input)
            if not medico_existe(dni_temp):
                print("El medico no esta en la lista. Intente de nuevo.")
                FuncionesGenerales.pausar()
                MostrartablaMedicos()
            else:
                medico1_dni = dni_temp
        except ValueError:
            print("Error: DNI debe ser un número.")

    # --- Pedir SEGUNDO MÉDICO ---
    print("\nPASO 2: Seleccione al SEGUNDO médico de la lista:")
    FuncionesGenerales.pausar()
    MostrartablaMedicos()
    
    medico2_dni = None
    while medico2_dni is None:
        try:
            dni_input = input("Ingresar DNI del SEGUNDO Médico (o 's' para volver): ")
            if dni_input.lower() == 's': return
            dni_temp = int(dni_input)
            if not medico_existe(dni_temp):
                print("El medico no esta en la lista. Intente de nuevo.")
                FuncionesGenerales.pausar()
                MostrartablaMedicos()
            elif dni_temp == medico1_dni:
                 print("Los medicos son los mismos, eliga otro por favor.")
                 FuncionesGenerales.pausar()
                 MostrartablaMedicos()
            else:
                medico2_dni = dni_temp
        except ValueError:
            print("Error: DNI debe ser un número.")

    # --- Lógica de Comparación ---
    FuncionesGenerales.limpiar_pantalla()
    print("--- Resultados de la Comparación ---")

    # --- CORRECCIÓN ---
    # Llamamos al helper del archivo de app (que usa gestor_datos.datos)
    comparacion = gestor_datos.comparar_medicos_historial(medico1_dni, medico2_dni)

    comunes = comparacion["comunes"]
    exclusivosPrimero = comparacion["solo_medico1"]
    exclusivosSegundo = comparacion["solo_medico2"]

    print("\nPacientes en común:")
    if not comunes: print("  (Ninguno)")
    for dni_paciente in comunes:
        # --- CORRECCIÓN ---
        paciente = gestor_datos.obtener_paciente(dni_paciente)
        if paciente:
            print(f"  {paciente['Nombre']} (DNI: {paciente['DNI']})")

    print(f"\nPacientes exclusivos del Dr. (DNI {medico1_dni}):")
    if not exclusivosPrimero: print("  (Ninguno)")
    for dni_paciente in exclusivosPrimero:
        # --- CORRECCIÓN ---
        paciente = gestor_datos.obtener_paciente(dni_paciente)
        if paciente:
            print(f"  {paciente['Nombre']} (DNI: {paciente['DNI']})")

    print(f"\nPacientes exclusivos del Dr. (DNI {medico2_dni}):")
    if not exclusivosSegundo: print("  (Ninguno)")
    for dni_paciente in exclusivosSegundo:
        # --- CORRECCIÓN ---
        paciente = gestor_datos.obtener_paciente(dni_paciente)
        if paciente:
            print(f"  {paciente['Nombre']} (DNI: {paciente['DNI']})")

    print("\n" + "=" * 50)
    FuncionesGenerales.pausar()
    # No limpiamos pantalla aquí, dejamos que el bucle principal lo haga

def buscarMedico():
    medico = FuncionesGenerales.buscar_persona(
        gestor_datos.listar_medicos(), tipo_busqueda="ambos"
    )
    if medico:
        visualizarDatos(medico, Encabezado="Datos del médico encontrado:")
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return medico
    return None


"""
Opción 7 (menu)
"""
def verTurnosMedico():
    FuncionesGenerales.limpiar_pantalla()
    while True:
        MostrartablaMedicos()
        dni = FuncionesGenerales.CargarDNI("medico")

        existe = medico_existe(dni)
        if not existe:
            print("El medico no esta en la lista")
            FuncionesGenerales.pausar()
            FuncionesGenerales.limpiar_pantalla()
            continue

        medico_data = gestor_datos.obtener_medico(dni)
        nombre_medico = medico_data["Nombre"]

        turnos_filtrados = filter(
            lambda t: t["medico_dni"] == dni and t["estado"] == "Confirmado",
            gestor_datos.listar_turnos(),
        )
        total_turnos = reduce(lambda count, turno: count + 1, turnos_filtrados, 0)

        print("=" * 40)
        print(f"Médico: {nombre_medico}")
        print(f"DNI: {dni}")
        print(f"Total de turnos confirmados: {total_turnos}")
        print("=" * 40)
        FuncionesGenerales.pausar()
        FuncionesGenerales.limpiar_pantalla()
        return

def fechaDeNacimientoMedico():
    while True:
        fecha=FuncionesGenerales.CargarFechaDeNacimiento()
        if FuncionesGenerales.CalculoEdad(fecha) < 25:
            print("Un medico no puede tener menos de 25 años")
        else:
            return fecha

def main(): ...


main()
