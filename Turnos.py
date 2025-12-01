import FuncionesGenerales as FG
import Pacientes
import Medicos
import gestor_datos
from datetime import date, timedelta, datetime

# Constantes para visualización
MESES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def _es_bisiesto(anio):
    """Retorna True si el año es bisiesto (regla gregoriana)."""
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

def _dias_en_mes(anio, mes):
    """Devuelve cuántos días tiene un mes específico."""
    # Índice 0 vacío para que coincida mes 1 con Enero
    dias = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Ajuste Febrero bisiesto
    if mes == 2 and _es_bisiesto(anio):
        return 29
    return dias[mes]

def _generar_matriz_mes(anio, mes):
    # 1. Averiguar qué día de la semana cae el 1ro (0=Lunes ... 6=Domingo)
    primer_dia_obj = date(anio, mes, 1)
    dia_inicio_semana = primer_dia_obj.weekday()
    
    total_dias = _dias_en_mes(anio, mes)
    
    lista_dias = [0] * dia_inicio_semana
    lista_dias.extend(range(1, total_dias + 1))
    
    # 3. Agrupar en semanas de 7 días
    matriz = []
    semana_actual = []
    
    for dia in lista_dias:
        semana_actual.append(dia)
        if len(semana_actual) == 7:
            matriz.append(semana_actual)
            semana_actual = []
            
    # 4. Rellenar última semana si quedó incompleta
    if semana_actual:
        while len(semana_actual) < 7:
            semana_actual.append(0)
        matriz.append(semana_actual)
        
    return matriz

# --- LÓGICA DE TURNOS ---

def obtener_slots(medico_dni, fecha_tuple):
    """
    Devuelve lista de horarios disponibles.
    Filtra los horarios ocupados Y los horarios pasados (si es hoy).
    """
    medico = gestor_datos.obtener_medico(medico_dni)
    if not medico or "Horarios" not in medico: return []

    nombres_dias = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    f_obj = date(*fecha_tuple)
    nombre_dia = nombres_dias[f_obj.weekday()]

    horario_dia = medico["Horarios"].get(nombre_dia)
    if not horario_dia: return [] # El médico no trabaja ese día

    hora_inicio, hora_fin = horario_dia
    slots = []
    
    hora_actual = hora_inicio
    minuto_actual = 0
    
    # Cargamos turnos ocupados de la BD
    ocupados = set()
    for t in gestor_datos.listar_turnos():
        if t["medico_dni"] == medico_dni and t["estado"] == "Confirmado":
            ocupados.add((tuple(t["fecha"]), tuple(t["hora"])))
    
    ahora_mismo = datetime.now()

    # Generamos los slots de 30 mins
    while hora_actual < hora_fin:
        slot_tiempo = (hora_actual, minuto_actual)
        
        # 1. Chequeo de base de datos
        esta_ocupado = (fecha_tuple, slot_tiempo) in ocupados
        
        # 2. Chequeo de tiempo real (No mostrar horarios pasados)
        fecha_hora_slot = datetime(fecha_tuple[0], fecha_tuple[1], fecha_tuple[2], hora_actual, minuto_actual)
        es_pasado = fecha_hora_slot < ahora_mismo

        if not esta_ocupado and not es_pasado:
            slots.append(slot_tiempo)

        # Avanzar 30 mins
        minuto_actual += 30
        if minuto_actual == 60:
            minuto_actual = 0
            hora_actual += 1
            
    return slots

def visualizar_calendario_grafico(medico_dni):
    """Muestra el calendario visual usando la matriz manual."""
    medico = gestor_datos.obtener_medico(medico_dni)
    FG.limpiar_pantalla()
    print("=" * 80)
    print(f" CALENDARIO DE DISPONIBILIDAD: Dr/a. {medico['Nombre']} ".center(80))
    print("=" * 80)
    print(" REFERENCIA: [Día (Turnos Libres)] | --- : Sin atención/Pasado \n")

    hoy = date.today()
    header_dias = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"]

    # Mostramos mes actual y siguiente
    for delta in range(2):
        mes_calc = hoy.month + delta
        anio_calc = hoy.year
        if mes_calc > 12:
            mes_calc -= 12
            anio_calc += 1
            
        nombre_mes = MESES[mes_calc]
        print(f"   >>>  {nombre_mes.upper()} {anio_calc}  <<<")
        
        # Manera de alinear cabecera 
        linea_head = " "
        for d in header_dias:
            linea_head += f"{d:^10}"
        print(linea_head)
        print(" " + "-"*70)

        # Generación de matriz propia
        matriz = _generar_matriz_mes(anio_calc, mes_calc)

        for semana in matriz:
            linea = " "
            for dia in semana:
                texto_celda = "---"
                if dia != 0:
                    fecha_iter = date(anio_calc, mes_calc, dia)
                    
                    if fecha_iter >= hoy:
                        ft = (anio_calc, mes_calc, dia)
                        cant = len(obtener_slots(medico_dni, ft))
                        if cant > 0:
                            texto_celda = f"[{dia:02d}({cant})]"
                        else:
                            texto_celda = f"[{dia:02d} (0)]"
                    else:
                        # Día pasado visual
                        texto_celda = f" {dia:02d} .."
                
                linea += f"{texto_celda:^10}"
            print(linea)
            print(" " + "-"*70)
        print("\n")

def agendar_turno():
    while True:
        # 1. Paciente
        Pacientes.mostrar_lista_pacientes()
        print("\n[BUSCAR PACIENTE] Enter para iniciar (o '0' para salir):")
        if input("> ") == "0": return
        
        paciente = FG.buscar_persona_ui(gestor_datos.listar_pacientes())
        if not paciente: continue
        
        FG.limpiar_pantalla()
        print(f"Paciente: {paciente['Nombre']}")
        FG.pausar()

        # 2. Médico
        Medicos.mostrar_tabla_medicos()
        print("\n[BUSCAR MÉDICO] Enter para seleccionar:")
        input("> ")
        
        medico = FG.buscar_persona_ui(gestor_datos.listar_medicos())
        if not medico: continue
        
        if medico['DNI'] == paciente['DNI']:
            print("\nError: El médico no puede atenderse a sí mismo.")
            FG.pausar()
            continue

        visualizar_calendario_grafico(medico['DNI'])
        
        print("Ingrese fecha (DD/MM/AAAA) o '0' para cancelar:")
        fi = input("> ")
        if fi == "0": continue
        
        try:
            fi = fi.replace("-", "/")
            d, m, a = map(int, fi.split("/"))
            fecha_turno = (a, m, d)
            
            if date(a, m, d) < date.today():
                print("No puede viajar al pasado.")
                FG.pausar()
                continue
        except ValueError:
            print("Formato incorrecto.")
            FG.pausar()
            continue

        slots = obtener_slots(medico['DNI'], fecha_turno)
        
        if not slots:
            print(f"\nSin horarios disponibles para el {d}/{m}/{a}.")
            FG.pausar()
            continue
            
        FG.limpiar_pantalla()
        print(f"=== HORARIOS PARA {d}/{m}/{a} ===")
        for i, s in enumerate(slots, 1):
            print(f"[{i}] {s[0]:02d}:{s[1]:02d}", end="\t")
            if i % 4 == 0: print()
            
        print("\n" + "-" * 50)
        
        try:
            sel = int(input("\nElija horario: "))
            if not (1 <= sel <= len(slots)): raise ValueError
            hora_elegida = slots[sel - 1]
            
            # Doble chequeo de seguridad
            dt_check = datetime(a, m, d, hora_elegida[0], hora_elegida[1])
            if dt_check < datetime.now():
                print("Error: Ese horario ya pasó hace instantes.")
                FG.pausar()
                continue
                
        except ValueError:
            print("Selección inválida.")
            FG.pausar()
            continue
            
        # 5. Confirmar
        FG.limpiar_pantalla()
        print("📝 CONFIRMAR TURNO")
        print(f" Paciente: {paciente['Nombre']}")
        print(f" Médico:   {medico['Nombre']}")
        print(f" Cita:     {d}/{m}/{a} a las {hora_elegida[0]:02d}:{hora_elegida[1]:02d}")
        
        if FG.confirmar_accion("¿Confirmar?"):
            nt = {
                "medico_dni": medico['DNI'],
                "paciente_dni": paciente['DNI'],
                "fecha": fecha_turno,
                "hora": hora_elegida,
                "estado": "Confirmado"
            }
            tid = gestor_datos.agregar_turno(nt)
            gestor_datos.agregar_historial(medico['DNI'], paciente['DNI'], tid, fecha_turno)
            print("\nTurno agendado.")
            FG.pausar()
            return

def cancelar_turno():
    FG.limpiar_pantalla()
    print("=== CANCELAR TURNO ===")
    Pacientes.mostrar_lista_pacientes()
    print("\nBusque al paciente:")
    
    paciente = FG.buscar_persona_ui(gestor_datos.listar_pacientes())
    if not paciente: return
    
    turnos = gestor_datos.buscar_turnos_por_paciente(paciente['DNI'])
    if not turnos:
        print("\nℹSin turnos pendientes.")
        FG.pausar()
        return
        
    FG.limpiar_pantalla()
    print(f"Turnos de: {paciente['Nombre']}")
    print("-" * 60)
    for t in turnos:
        m = gestor_datos.obtener_medico(t['medico_dni'])
        f = t['fecha']; h = t['hora']
        print(f"[ID: {t['id']}] {f[2]}/{f[1]} {h[0]:02d}:{h[1]:02d} - Dr. {m['Nombre']}")
    print("-" * 60)
        
    try:
        tid = int(input("\nID a cancelar (0 salir): "))
        if tid == 0: return
        if not any(x['id'] == tid for x in turnos):
            print("ID inválido.")
            FG.pausar()
            return
            
        if FG.confirmar_accion("¿Cancelar?"):
            gestor_datos.cancelar_turno(tid)
            gestor_datos.actualizar_estado_historial(tid, "Cancelado")
            print("Cancelado.")
            FG.pausar()
    except ValueError:
        print("Error.")
        FG.pausar()

def ver_turnos_paciente():
    FG.limpiar_pantalla()
    Pacientes.mostrar_lista_pacientes()
    print("\nSeleccione paciente:")
    paciente = FG.buscar_persona_ui(gestor_datos.listar_pacientes())
    if not paciente: return
    
    FG.limpiar_pantalla()
    print(f"HISTORIAL: {paciente['Nombre']}")
    todos = [t for t in gestor_datos.listar_turnos() if t["paciente_dni"] == paciente['DNI']]
    if not todos:
        print("Vacío.")
    else:
        todos.sort(key=lambda x: tuple(x["fecha"]))
        print(f"{'FECHA':<12} {'HORA':<8} {'MÉDICO':<20} {'ESTADO'}")
        print("-" * 60)
        for t in todos:
            m = gestor_datos.obtener_medico(t['medico_dni'])
            f = t['fecha']; h = t['hora']
            nom_med = m['Nombre'] if m else "Desconocido"
            print(f"{f[2]:02d}/{f[1]:02d}/{f[0]:<4} {h[0]:02d}:{h[1]:02d}   {nom_med[:20]:<20} {t['estado']}")
    FG.pausar()