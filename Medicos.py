import FuncionesGenerales as FG
import gestor_datos
from datetime import date

# --- VISUALIZACIÓN ---

def visualizar_datos_medico(medico, encabezado="DATOS DEL MÉDICO"):
    FG.limpiar_pantalla()
    print("=" * 60)
    print(encabezado.center(60))
    print("=" * 60)
    
    # Blindaje contra datos faltantes
    f_nac = medico.get('Fecha de Nacimiento')
    edad = FG.calcular_edad(f_nac) if f_nac else "??"
    
    print(f" Nombre:        {medico.get('Nombre', 'Desconocido')}")
    print(f" DNI:           {medico.get('DNI', 0)}")
    print(f" Edad:          {edad} años")
    print(f" Especialidad:  {medico.get('Especialidad', 'Sin asignar')}")
    print(f" Estado:        {medico.get('Estado', 'Disponible')}")
    
    print("\n [Horarios de Atención]")
    horarios = medico.get("Horarios", {})
    if horarios:
        dias_orden = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for dia in dias_orden:
            if dia in horarios and horarios[dia]:
                inicio, fin = horarios[dia]
                print(f"   ├─ {dia:<10}: {inicio:02d}:00 a {fin:02d}:00 hs")
    else:
        print("   (No hay horarios definidos)")
    print("=" * 60)

def mostrar_tabla_medicos():
    FG.limpiar_pantalla()
    ancho = 110
    print("=" * ancho)
    print("STAFF MÉDICO".center(ancho))
    print("=" * ancho)
    print(f"{'DNI':<12} {'Nombre':<25} {'Especialidad':<30} {'Turnos Hoy':<12} {'Estado':<10}")
    print("-" * ancho)
    
    lista = gestor_datos.listar_medicos()
    hoy_tuple = (date.today().year, date.today().month, date.today().day)
    
    for m in lista:
        dni = m.get('DNI', 0)
        
        # Contamos turnos hoy
        turnos_hoy = len([t for t in gestor_datos.listar_turnos() 
                          if t["medico_dni"] == dni 
                          and tuple(t["fecha"]) == hoy_tuple 
                          and t["estado"] == "Confirmado"])
        
        nom = m.get('Nombre', 'Desconocido')
        esp = m.get('Especialidad', '---')
        est = m.get('Estado', '---')
        
        print(f"{dni:<12} {nom:<25} {esp:<30} {turnos_hoy:<12} {est:<10}")
    
    print("=" * ancho)
    # --- CORRECCIÓN: Agregamos pausa para que el usuario alcance a leer ---
    FG.pausar() 

# --- INPUTS ---

def cargar_especialidad_ui():
    print("=" * 40)
    print("Seleccione Especialidad:")
    lista = gestor_datos.especialidades_medicas
    for i, esp in enumerate(lista, 1):
        print(f"[{i}] {esp}")
    print("=" * 40)
    
    while True:
        try:
            op = int(input("Opción: "))
            if 1 <= op <= len(lista):
                return lista[op - 1]
            print("Opción inválida.")
        except ValueError:
            print("Ingrese un número.")

def validar_edad_minima_medico():
    while True:
        fecha = FG.cargar_fecha_nacimiento()
        if FG.calcular_edad(fecha) < 25:
            print("Error: El médico debe tener al menos 25 años.")
        else:
            return fecha

# --- ALGORITMOS RECURSIVOS ---

def _imprimir_historial_recursivo(historial, indice=0):
    """
    Imprime una lista de historial clínico de forma recursiva con formato visual de árbol.

    Esta función recorre la lista 'historial' elemento por elemento utilizando un índice,
    sin usar bucles tradicionales (for/while). Muestra los datos de cada turno y 
    dibuja líneas conectoras para simular una estructura jerárquica.

    Args:
        historial (list): Lista de diccionarios, donde cada diccionario representa un registro
                          del historial (contiene fecha, dni paciente, estado, etc.).
        indice (int, opcional): Posición actual en la lista que se está procesando. 
                                Por defecto inicia en 0.

    Returns:
        None: La función no retorna valores, imprime directamente en consola.
    """
    
    # --- CASO BASE (Condición de parada) ---
    # Si el índice actual es igual o mayor al tamaño de la lista, significa que
    # ya hemos procesado todos los elementos.
    if indice >= len(historial):
        # Imprimimos la línea final ("pie") del árbol para cerrar el dibujo visualmente.
        print("    " + "└──" + "─" * 50) 
        return  # Terminamos la ejecución de la función (rompemos la recursión).

    # --- PROCESAMIENTO DEL ELEMENTO ACTUAL ---
    # Obtenemos el registro correspondiente a la posición actual del índice.
    item = historial[indice]
    
    # Buscamos los datos completos del paciente usando su DNI para mostrar el nombre.
    # Si el paciente no existe (borrado), mostramos el DNI como respaldo.
    p = gestor_datos.obtener_paciente(item["paciente_dni"])
    nombre_p = p["Nombre"] if p else f"DNI {item['paciente_dni']}"
    
    # Formateamos la fecha almacenada como tupla [año, mes, día] a string "DD/MM/AAAA".
    fecha = item['fecha']
    fecha_str = f"{fecha[2]:02d}/{fecha[1]:02d}/{fecha[0]}"
    
    # Obtenemos el estado del turno (ej: "Confirmado", "Cancelado").
    estado = item['estado']

    # Definimos el conector visual para las ramas intermedias del árbol.
    conector = "├──" 
    
    # Imprimimos la fila con formato alineado.
    # :<20 asegura que el nombre ocupe siempre 20 espacios para mantener la tabla ordenada.
    print(f"    {conector} FECHA: {fecha_str} | PACIENTE: {nombre_p:<20} | ESTADO: {estado}")

    # --- LLAMADA RECURSIVA (Paso al siguiente) ---
    # La función se llama a sí misma, pero incrementando el índice en 1.
    # Esto mueve el "puntero" al siguiente elemento de la lista.
    _imprimir_historial_recursivo(historial, indice + 1)

# --- ACCIONES ---

def agregar_medico():
    FG.limpiar_pantalla()
    while True:
        # Llamamos a mostrar tabla pero ignoramos su pausa interna limpiando pantalla luego
        # (Aunque ahora pedirá un Enter extra, es preferible a que no funcione el menú principal)
        mostrar_tabla_medicos() 
        FG.limpiar_pantalla() 
        
        print("\n" + "="*30) 
        print("   ALTA DE MÉDICO")
        print("="*30)
        
        dni = FG.cargar_dni("médico")
        
        if gestor_datos.obtener_medico(dni):
            print("Ya existe un médico con ese DNI.")
            FG.pausar()
            return

        nombre = FG.cargar_nombre()
        fecha_nac = validar_edad_minima_medico()
        FG.limpiar_pantalla()
        especialidad = cargar_especialidad_ui()
        
        horarios_default = {
            "Lunes": [9, 18], "Martes": [9, 18], "Miércoles": [9, 18],
            "Jueves": [9, 18], "Viernes": [9, 18]
        }

        nuevo_medico = {
            "Nombre": nombre,
            "DNI": dni,
            "Fecha de Nacimiento": fecha_nac,
            "Especialidad": especialidad,
            "Horarios": horarios_default,
            "Estado": "Disponible"
        }

        visualizar_datos_medico(nuevo_medico, "CONFIRMAR ALTA")
        
        if FG.confirmar_accion("¿Confirmar?", "Alta cancelada."):
            gestor_datos.agregar_medico(nuevo_medico)
            print(f"\nMédico {nombre} registrado con éxito.")
            FG.pausar()
            break

def eliminar_medico():
    while True:
        mostrar_tabla_medicos()
        print("\n--- BAJA DE MÉDICO ---")
        dni = FG.cargar_dni("médico a eliminar")
        
        medico = gestor_datos.obtener_medico(dni)
        if not medico:
            print("Médico no encontrado.")
            FG.pausar()
            continue
            
        visualizar_datos_medico(medico, "ATENCIÓN: SE ELIMINARÁ ESTE MÉDICO")
        print("NOTA: Si esta persona no es paciente, sus datos personales también se borrarán.")
        
        if FG.confirmar_accion("¿Eliminar rol médico?", "Cancelado."):
            gestor_datos.eliminar_medico(dni)
            print("Médico dado de baja.")
            FG.pausar()
            return

def modificar_medico():
    while True:
        mostrar_tabla_medicos()
        print("\n--- MODIFICAR MÉDICO ---")
        dni = FG.cargar_dni("médico a modificar")
        original = gestor_datos.obtener_medico(dni)
        
        if not original:
            print("Médico no encontrado.")
            FG.pausar()
            continue
            
        print(f"\nModificando a: {original['Nombre']}")
        print("Ingrese nuevos datos:")
        nombre = FG.cargar_nombre()
        especialidad = cargar_especialidad_ui()
        
        cambios = {
            "Nombre": nombre,
            "Especialidad": especialidad
        }
        
        preview = original.copy()
        preview.update(cambios)
        visualizar_datos_medico(preview, "VISTA PREVIA")
        
        if FG.confirmar_accion("¿Guardar cambios?"):
            gestor_datos.modificar_medico(dni, cambios)
            print("Datos modificados.")
            FG.pausar()
            return

# --- HISTORIALES Y COMPARACIÓN ---

def _obtener_nombres_de_dnis(conjunto_dnis):
    nombres = []
    for dni in conjunto_dnis:
        p = gestor_datos.obtener_paciente(dni)
        if p:
            nombres.append(p['Nombre'])
        else:
            nombres.append(str(dni))
    return nombres

def mostrar_historial_medico():
    FG.limpiar_pantalla()
    print("=== GESTIÓN DE HISTORIALES ===")
    print("[1] Ver historial clínico (Recursivo)")
    print("[2] Comparar pacientes entre médicos")
    print("[0] Volver")
    op = input("Ingrese su opción: ")
    
    if op == "1":
        mostrar_tabla_medicos() 
        print("\nIngrese el DNI del médico para ver su historial:")
        dni = FG.cargar_dni("médico")
        
        medico = gestor_datos.obtener_medico(dni)
        if not medico:
            print("Médico no encontrado.")
            FG.pausar(); return

        historial = gestor_datos.obtener_historial_por_medico(dni)
        
        FG.limpiar_pantalla()
        print(f"HISTORIAL CLÍNICO: Dr/a. {medico['Nombre']}")
        print("=" * 60)
        
        if not historial:
            print("   (El historial está vacío)")
        else:
            historial.sort(key=lambda x: tuple(x['fecha']))
            print("    ┌" + "─" * 50)
            _imprimir_historial_recursivo(historial, 0)
            
        print("\n")
        FG.pausar()
        
    elif op == "2":
        FG.limpiar_pantalla()
        print("SELECCIONE LOS MÉDICOS A COMPARAR:")
        print("-" * 40)
        mostrar_tabla_medicos() 
        
        print("\n--- Médico A ---")
        dni1 = FG.cargar_dni("primer médico")
        m1 = gestor_datos.obtener_medico(dni1)
        
        print("\n--- Médico B ---")
        dni2 = FG.cargar_dni("segundo médico")
        m2 = gestor_datos.obtener_medico(dni2)
        
        if not m1 or not m2:
            print("Uno de los médicos no existe.")
            FG.pausar(); return

        if dni1 == dni2:
            print("Error: Son el mismo médico.")
            FG.pausar(); return

        res = gestor_datos.comparar_medicos_historial(dni1, dni2)
        
        nombres_comunes = _obtener_nombres_de_dnis(res['comunes'])
        nombres_solo1 = _obtener_nombres_de_dnis(res['solo_medico1'])
        nombres_solo2 = _obtener_nombres_de_dnis(res['solo_medico2'])
        
        FG.limpiar_pantalla()
        print("=" * 90)
        print(f" COMPARATIVA: {m1['Nombre']}  vs  {m2['Nombre']} ".center(90))
        print("=" * 90)
        
        print(f"\n[PACIENTES EN COMÚN] ({len(nombres_comunes)})")
        print("-" * 30)
        if not nombres_comunes: print(" - Ninguno")
        for n in nombres_comunes: print(f" * {n}")
            
        print(f"\n[SOLO ATENDIDOS POR {m1['Nombre'].upper()}] ({len(nombres_solo1)})")
        print("-" * 30)
        if not nombres_solo1: print(" - Ninguno")
        for n in nombres_solo1: print(f" * {n}")
            
        print(f"\n[SOLO ATENDIDOS POR {m2['Nombre'].upper()}] ({len(nombres_solo2)})")
        print("-" * 30)
        if not nombres_solo2: print(" - Ninguno")
        for n in nombres_solo2: print(f" * {n}")
        
        print("\n" + "=" * 90)
        FG.pausar()

def ver_turnos_medico():
    mostrar_tabla_medicos()
    print("\nIngrese DNI para ver detalles:")
    dni = FG.cargar_dni("médico")
    turnos = [t for t in gestor_datos.listar_turnos() if t["medico_dni"] == dni and t["estado"] == "Confirmado"]
    
    print(f"\nTotal turnos confirmados futuros: {len(turnos)}")
    FG.pausar()

def buscar_medico():
    encontrado = FG.buscar_persona_ui(gestor_datos.listar_medicos())
    if encontrado:
        visualizar_datos_medico(encontrado)
        FG.pausar()