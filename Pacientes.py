import gestor_datos
import FuncionesGenerales as FG
from datetime import date

# --- FUNCIONES AUXILIARES ---

def _formatear_edad_dinamica(fecha_tuple):
    """
    Calcula la edad exacta. 
    - Si es menor a 1 año, devuelve meses (ej: "8 meses").
    - Si es mayor a 1 año, devuelve años (ej: "5 años").
    """
    if not fecha_tuple: return "??"
    
    hoy = date.today()
    nac = date(*fecha_tuple) # Desempaquetamos la tupla (anio, mes, dia)
    
    # Cálculo total de meses vividos
    diferencia_meses = (hoy.year - nac.year) * 12 + (hoy.month - nac.month)
    
    # Ajuste por día (si no ha pasado el día de cumpleaños en el mes actual)
    if hoy.day < nac.day:
        diferencia_meses -= 1
        
    if diferencia_meses < 0: return "Recién nacido"
    
    # Lógica de visualización
    if diferencia_meses < 12:
        return f"{diferencia_meses} meses"
    else:
        anios = diferencia_meses // 12
        unidad = "año" if anios == 1 else "años"
        return f"{anios} {unidad}"

def cargar_obra_social_ui(es_medico=False):
    print("=" * 40)
    print("Seleccione una Obra Social:")
    
    lista = gestor_datos.obras_y_prepagas_arg.copy()
    
    if es_medico:
        lista.insert(0, "Hospital (Cobertura Interna)")
    
    for i, obra in enumerate(lista, 1):
        print(f"[{i}] {obra}")
    print("=" * 40)

    while True:
        try:
            opcion = int(input("Ingrese su opción: "))
            if 1 <= opcion <= len(lista):
                return lista[opcion - 1]
            print("Opción fuera de rango.")
        except ValueError:
            print("Debe ingresar un número.")

# --- VISUALIZACIÓN DE DATOS ---

def visualizar_datos_paciente(paciente, encabezado="DATOS DEL PACIENTE"):  
    FG.limpiar_pantalla()
    print("=" * 60)
    print(f"{encabezado}".center(60))
    print("=" * 60)
    
    f_nac = paciente.get('Fecha de Nacimiento')
    
    # Usamos la nueva lógica dinámica para la edad
    edad_str = _formatear_edad_dinamica(f_nac)
    
    if f_nac:
        fecha_str = f"{f_nac[2]:02d}/{f_nac[1]:02d}/{f_nac[0]}"
    else:
        fecha_str = "Desconocida"

    print(f" DNI:              {paciente.get('DNI', 0)}")
    print(f" Nombre:           {paciente.get('Nombre', 'Desconocido')}")
    print(f" F. Nacimiento:    {fecha_str}")
    print(f" Edad:             {edad_str}")  # <--- Aquí se ve el cambio (meses/años)
    print(f" Obra Social:      {paciente.get('Obra Social', '---')}")
    print("=" * 60)

def mostrar_lista_pacientes():
    FG.limpiar_pantalla()
    ancho = 110
    print("=" * ancho)
    print("LISTADO DE PACIENTES".center(ancho))
    print("=" * ancho)
    print(f"{'DNI':<12} {'Nombre':<30} {'Edad':<15} {'Obra Social':<40}")
    print("-" * ancho)
    
    lista = gestor_datos.listar_pacientes()
    
    if not lista:
        print("No hay pacientes registrados.".center(ancho))

    for p in lista:
        f_nac = p.get('Fecha de Nacimiento')
        edad_str = _formatear_edad_dinamica(f_nac) # <--- Uso en listado
        
        nombre = p.get('Nombre', 'Desconocido')
        dni = p.get('DNI', 0)
        obra = p.get('Obra Social', '---')
        
        print(f"{dni:<12} {nombre:<30} {edad_str:<15} {obra:<40}")
    
    print("=" * ancho)
    FG.pausar()

def ver_historial_completo(paciente_dni=None):
    """
    Muestra una tabla detallada cruzando datos de turnos y médicos.
    """
    if paciente_dni is None:
        mostrar_lista_pacientes()
        print("\nIngrese DNI para ver historial detallado (0 para volver):")
        try:
            paciente_dni = int(input("> "))
            if paciente_dni == 0: return
        except: return

    paciente = gestor_datos.obtener_paciente(paciente_dni)
    if not paciente:
        print("Paciente no encontrado.")
        FG.pausar(); return

    # Buscar turnos del paciente (historial)
    todos_turnos = [t for t in gestor_datos.listar_turnos() if t["paciente_dni"] == paciente_dni]
    
    FG.limpiar_pantalla()
    print("=" * 100)
    print(f" HISTORIA CLÍNICA: {paciente['Nombre']} (Obra Social: {paciente.get('Obra Social','-')}) ".center(100))
    print("=" * 100)

    if not todos_turnos:
        print("\n    El paciente no tiene historial de turnos registrados.\n")
    else:
        # Ordenar por fecha
        todos_turnos.sort(key=lambda x: tuple(x["fecha"]))
        
        # Cabecera de la tabla mejorada
        print(f"{'FECHA':<12} {'HORA':<6} {'ESPECIALIDAD':<25} {'MÉDICO':<25} {'ESTADO':<15}")
        print("-" * 100)
        
        for t in todos_turnos:
            # Cruzamos datos con Medicos para sacar Especialidad y Nombre
            medico = gestor_datos.obtener_medico(t['medico_dni'])
            
            f = t['fecha']
            h = t['hora']
            
            fecha_fmt = f"{f[2]:02d}/{f[1]:02d}/{f[0]}"
            hora_fmt = f"{h[0]:02d}:{h[1]:02d}"
            
            # Datos del médico (con blindaje .get)
            esp = medico.get('Especialidad', 'Desconocida') if medico else "Dr. no encontrado"
            nom_med = medico.get('Nombre', '---') if medico else "---"
            estado = t.get('estado', 'Desconocido')
            
            print(f"{fecha_fmt:<12} {hora_fmt:<6} {esp[:24]:<25} {nom_med[:24]:<25} {estado:<15}")
            
    print("=" * 100)
    FG.pausar()

# --- ACCIONES CRUD ---

def agregar_paciente():
    FG.limpiar_pantalla()
    while True:
        mostrar_lista_pacientes()
        print("\n--- NUEVO PACIENTE ---")
        
        dni = FG.cargar_dni("paciente")
        
        if gestor_datos.obtener_paciente(dni):
            print(f"Ya existe un paciente con el DNI {dni}.")
            FG.pausar()
            return

        medico_existente = gestor_datos.obtener_medico(dni)
        
        if medico_existente:
            FG.limpiar_pantalla()
            print("="*50)
            print("¡ATENCIÓN! DNI ENCONTRADO EN BASE DE DATOS".center(50))
            print("="*50)
            print(f"Este DNI corresponde a un Médico ya registrado:")
            print(f"Nombre:       {medico_existente['Nombre']}")
            print(f"Especialidad: {medico_existente['Especialidad']}")
            print("-" * 50)
            
            if FG.confirmar_accion(f"¿Desea dar de alta al Dr/a. {medico_existente['Nombre']} como paciente?", "Alta cancelada."):
                nombre = medico_existente['Nombre']
                f_nac = medico_existente['Fecha de Nacimiento']
                
                print(f"\nSeleccione la cobertura para el paciente (Se incluye opción 'Hospital' por ser personal):")
                obra_social = cargar_obra_social_ui(es_medico=True)
                
                nuevo_paciente = {
                    "DNI": dni,
                    "Nombre": nombre,
                    "Fecha de Nacimiento": f_nac,
                    "Obra Social": obra_social
                }
                
                gestor_datos.agregar_paciente(nuevo_paciente)
                print(f"Paciente agregado exitosamente con cobertura: {obra_social}")
                FG.pausar()
                break
            else:
                return

        nombre = FG.cargar_nombre()
        f_nac = FG.cargar_fecha_nacimiento()
        FG.limpiar_pantalla()
        obra_social = cargar_obra_social_ui(es_medico=False)

        nuevo_paciente = {
            "DNI": dni,
            "Nombre": nombre,
            "Fecha de Nacimiento": f_nac,
            "Obra Social": obra_social
        }

        visualizar_datos_paciente(nuevo_paciente, "CONFIRMAR NUEVO PACIENTE")
        
        if FG.confirmar_accion("¿Confirmar alta?", "Alta cancelada."):
            gestor_datos.agregar_paciente(nuevo_paciente)
            print("Paciente registrado correctamente.")
            FG.pausar()
            break

def eliminar_paciente():
    while True:
        mostrar_lista_pacientes()
        print("\n--- ELIMINAR PACIENTE ---")
        dni = FG.cargar_dni("paciente a eliminar")

        paciente = gestor_datos.obtener_paciente(dni)
        if not paciente:
            print("Paciente no encontrado.")
            FG.pausar()
            continue

        visualizar_datos_paciente(paciente, "ATENCIÓN: SE ELIMINARÁ ESTE PACIENTE")
        print("NOTA: Si esta persona también es médico, ese rol NO se borrará.")
        
        if FG.confirmar_accion("¿Está seguro?", "Eliminación cancelada."):
            gestor_datos.eliminar_paciente(dni)
            print("Paciente eliminado.")
            FG.pausar()
            return

def modificar_paciente():
    while True:
        mostrar_lista_pacientes()
        print("\n--- MODIFICAR PACIENTE ---")
        dni = FG.cargar_dni("paciente a modificar")

        original = gestor_datos.obtener_paciente(dni)
        if not original:
            print("Paciente no encontrado.")
            FG.pausar()
            continue

        print("\nIngrese los nuevos datos (Los datos anteriores se perderán):")
        
        es_medico = gestor_datos.obtener_medico(dni) is not None
        if es_medico:
            print("NOTA: Este paciente es MÉDICO. La fecha de nacimiento debe cumplir con la edad mínima (25 años).")
        
        nombre = FG.cargar_nombre()
        
        while True:
            f_nac = FG.cargar_fecha_nacimiento()
            if es_medico:
                edad_calc = FG.calcular_edad(f_nac)
                if edad_calc < 25:
                    print(f"ERROR: La edad calculada es {edad_calc} años. Un médico debe tener al menos 25.")
                    continue 
            break

        obra_social = cargar_obra_social_ui(es_medico=es_medico)

        modificado = {
            "Nombre": nombre,
            "Fecha de Nacimiento": f_nac,
            "Obra Social": obra_social
        }

        preview = original.copy()
        preview.update(modificado)
        visualizar_datos_paciente(preview, "VISTA PREVIA DE MODIFICACIÓN")

        if FG.confirmar_accion("¿Guardar cambios?", "Modificación cancelada."):
            gestor_datos.modificar_paciente(dni, modificado)
            print("Datos actualizados correctamente.")
            FG.pausar()
            return

def buscar_paciente():
    encontrado = FG.buscar_persona_ui(gestor_datos.listar_pacientes())
    if encontrado:
        visualizar_datos_paciente(encontrado, "PACIENTE ENCONTRADO")
        # Opcional: preguntar si quiere ver historial
        if FG.confirmar_accion("¿Ver historia clínica completa de este paciente?", ""):
            ver_historial_completo(encontrado['DNI'])
        else:
            FG.pausar()
        return encontrado
    return None