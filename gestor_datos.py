import json
from pathlib import Path

# --- CONFIGURACIÓN ---
STORAGE_DIR = Path(__file__).parent / "data"

FILES = {
    "personas": STORAGE_DIR / "personas.json",
    "medicos": STORAGE_DIR / "medicos.json",
    "pacientes": STORAGE_DIR / "pacientes.json",
    "turnos": STORAGE_DIR / "turnos.json",
    "historial": STORAGE_DIR / "historial.json",
    "especialidades": STORAGE_DIR / "especialidades.json",
    "obras_sociales": STORAGE_DIR / "obras_sociales.json",
}

# --- GESTIÓN DE ARCHIVOS ---
def inicializar_storage():
    """Crea directorios y archivos iniciales si no existen."""
    STORAGE_DIR.mkdir(exist_ok=True)
    
    lista_obras = [
        "APM / OSAPM","APRES Salud","APSOT / FFST","ASMEPRIV","Activa Salud","Andar","Assistravel","Avalian","Banco Provincia (BCO. PCIA.)",
        "Bristol / Santa Cecilia","C.A.S.A","CEMIC","CIMA","Cobermed","Cobertec / OS Mosaistas","Colegio de Escribanos Plan Especial (OSSEG)",
        "COMEI","Corporación Asistencial","DASMI - Universidad de Luján","Dom Centro de Reumatología","Emergencias","Empleados de Farmacia","Galeno",
        "IO SFA (Instituto de Obra Social de las Fuerzas Armadas)","Medicus","Medifé","OSDE","OSIPE","OSVARA","Obra Social de Petroleros Privados",
        "Obra Social del Personal de Edificios de Renta y Horizontal","Obras Sociales Unión Personal (UP)","Omint","PAMI","Particular","Premedic",
        "Prevención Salud","Salud y Bienestar","Sancor Salud","Swiss Medical"]

    defaults = {
        "especialidades": ["Alergología","Anestesiología","Cardiología","Cirugía General",
        "Cirugía Cardiovascular","Cirugía Plástica y Reconstructiva","Cirugía Pediátrica",
        "Cirugía Torácica","Cirugía Vascular","Dermatología","Endocrinología","Gastroenterología",
        "Geriatría","Ginecología y Obstetricia","Hematología","Hepatología","Infectología","Medicina de Emergencias",
        "Medicina del Deporte","Medicina Familiar y Comunitaria","Medicina Física y Rehabilitación","Medicina Intensiva",
        "Medicina Interna","Medicina Legal y Forense","Nefrología","Neumología","Neurología","Neurocirugía","Nutriología Clínica",
        "Oftalmología","Oncología Médica","Oncología Radioterápica","Ortopedia y Traumatología","Otorrinolaringología","Pediatría",
        "Psiquiatría","Radiología","Reumatología","Toxicología","Urología"],
        "obras_sociales": lista_obras,
        "personas": [],
        "medicos": [],
        "pacientes": [],
        "turnos": [],
        "historial": []
    }

    for key, ruta in FILES.items():
        if not ruta.exists():
            with open(ruta, "w", encoding="utf-8") as f:
                data_a_guardar = defaults.get(key, [])
                json.dump(data_a_guardar, f, indent=2, ensure_ascii=False)

def cargar_datos_raw():
    """Lee todos los archivos JSON y los carga en un diccionario."""
    cache = {}
    for key, ruta in FILES.items():
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                cache[key] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cache[key] = []
    return cache

def guardar_archivo(key, datos_lista):
    """Escribe una lista específica en el archivo JSON correspondiente."""
    try:
        with open(FILES[key], "w", encoding="utf-8") as f:
            json.dump(datos_lista, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando {key}: {e}")

# --- INICIALIZACIÓN DE VARIABLES GLOBALES ---
inicializar_storage()

# _memoria es un diccionario común y corriente
_memoria = cargar_datos_raw()

# Exponemos las listas de referencia
obras_y_prepagas_arg = _memoria.get("obras_sociales", [])
especialidades_medicas = _memoria.get("especialidades", [])

# --- FUNCIONES INTERNAS (LÓGICA DEL NEGOCIO) ---
def _crear_actualizar_persona(full_data):
    """Gestiona la lista de personas (unifica datos)."""
    dni = full_data["DNI"]
    nueva_p = {
        "DNI": dni,
        "Nombre": full_data["Nombre"],
        "Fecha de Nacimiento": full_data["Fecha de Nacimiento"]
    }
    
    lista = _memoria["personas"]
    idx = -1 # Porque este -1 es un indicador de "no encontrado"
    
    # Búsqueda secuencial
    for i in range(len(lista)):
        if lista[i]["DNI"] == dni:
            idx = i
            break
    
    if idx >= 0:
        lista[idx] = nueva_p # Actualizar
    else:
        lista.append(nueva_p) # Agregar
        
    guardar_archivo("personas", lista)

def _eliminar_persona_si_huerfana(dni):
    """
    Elimina los datos personales si el DNI ya no está ni en médicos ni en pacientes.
    (Autolimpieza).
    """
    es_medico = False
    for m in _memoria["medicos"]:
        if m["DNI"] == dni:
            es_medico = True
            break
            
    es_paciente = False
    for p in _memoria["pacientes"]:
        if p["DNI"] == dni:
            es_paciente = True
            break
    
    # Si no es nada, lo borramos
    if not es_medico and not es_paciente:
        # Filtramos la lista para sacar al DNI (creando una lista nueva sin él)
        nueva_lista_personas = []
        for p in _memoria["personas"]:
            if p["DNI"] != dni:
                nueva_lista_personas.append(p)
        
        _memoria["personas"] = nueva_lista_personas
        guardar_archivo("personas", _memoria["personas"])

def _unir(dni, datos_rol):
    """Busca los datos personales y los une al diccionario del rol."""
    persona = None
    for p in _memoria["personas"]:
        if p["DNI"] == dni:
            persona = p
            break
    
    if not persona:
        return datos_rol
    
    # Copiamos el diccionario para no modificar el original
    unido = datos_rol.copy()
    # Agregamos manualmente las claves que faltan
    unido["Nombre"] = persona["Nombre"]
    unido["Fecha de Nacimiento"] = persona["Fecha de Nacimiento"]
    return unido

# === MÉDICOS ===
def agregar_medico(full_data):
    # 1. Gestionar Persona
    _crear_actualizar_persona(full_data)
    
    # 2. Gestionar Médico
    rol = {
        "DNI": full_data["DNI"],
        "Especialidad": full_data["Especialidad"],
        "Horarios": full_data.get("Horarios", {}),
        "Estado": "Disponible"
    }
    _memoria["medicos"].append(rol)
    guardar_archivo("medicos", _memoria["medicos"])

def obtener_medico(dni):
    medico_encontrado = None
    for m in _memoria["medicos"]:
        if m["DNI"] == dni:
            medico_encontrado = m
            break
            
    if medico_encontrado:
        return _unir(dni, medico_encontrado)
    return None

def listar_medicos():
    lista_completa = []
    for m in _memoria["medicos"]:
        lista_completa.append(_unir(m["DNI"], m))
    return lista_completa

def eliminar_medico(dni):
    lista_nueva = []
    eliminado = False
    
    for m in _memoria["medicos"]:
        if m["DNI"] == dni:
            eliminado = True
        else:
            lista_nueva.append(m)
    
    if eliminado:
        _memoria["medicos"] = lista_nueva
        guardar_archivo("medicos", _memoria["medicos"])
        # Intentar autolimpieza
        _eliminar_persona_si_huerfana(dni)
        return True
    return False

def modificar_medico(dni, full_data):
    # Modificar Persona
    if "Nombre" in full_data: 
        persona = None
        for p in _memoria["personas"]:
            if p["DNI"] == dni:
                persona = p
                break
        if persona:
            if "Nombre" in full_data: persona["Nombre"] = full_data["Nombre"]
            if "Fecha de Nacimiento" in full_data: persona["Fecha de Nacimiento"] = full_data["Fecha de Nacimiento"]
            _crear_actualizar_persona(persona)

    # Modificar Médico
    medico = None
    for m in _memoria["medicos"]:
        if m["DNI"] == dni:
            medico = m
            break
            
    if medico:
        if "Especialidad" in full_data: medico["Especialidad"] = full_data["Especialidad"]
        if "Horarios" in full_data: medico["Horarios"] = full_data["Horarios"]
        guardar_archivo("medicos", _memoria["medicos"])
        return True
    return False

# === PACIENTES ===
def agregar_paciente(full_data):
    _crear_actualizar_persona(full_data)
    rol = { "DNI": full_data["DNI"], "Obra Social": full_data["Obra Social"] }
    _memoria["pacientes"].append(rol)
    guardar_archivo("pacientes", _memoria["pacientes"])

def obtener_paciente(dni):
    paciente_encontrado = None
    for p in _memoria["pacientes"]:
        if p["DNI"] == dni:
            paciente_encontrado = p
            break
            
    if paciente_encontrado:
        return _unir(dni, paciente_encontrado)
    return None

def listar_pacientes():
    lista_completa = []
    for p in _memoria["pacientes"]:
        lista_completa.append(_unir(p["DNI"], p))
    return lista_completa

def eliminar_paciente(dni):
    lista_nueva = []
    eliminado = False
    
    for p in _memoria["pacientes"]:
        if p["DNI"] == dni:
            eliminado = True
        else:
            lista_nueva.append(p)
    
    if eliminado:
        _memoria["pacientes"] = lista_nueva
        guardar_archivo("pacientes", _memoria["pacientes"])
        # Intentar autolimpieza
        _eliminar_persona_si_huerfana(dni)
        return True
    return False

def modificar_paciente(dni, full_data):
    # Modificar Persona
    if "Nombre" in full_data:
        persona = None
        for p in _memoria["personas"]:
            if p["DNI"] == dni:
                persona = p
                break
        if persona:
            if "Nombre" in full_data: persona["Nombre"] = full_data["Nombre"]
            if "Fecha de Nacimiento" in full_data: persona["Fecha de Nacimiento"] = full_data["Fecha de Nacimiento"]
            _crear_actualizar_persona(persona)
            
    # Modificar Paciente
    paciente = None
    for p in _memoria["pacientes"]:
        if p["DNI"] == dni:
            paciente = p
            break
            
    if paciente:
        if "Obra Social" in full_data: paciente["Obra Social"] = full_data["Obra Social"]
        guardar_archivo("pacientes", _memoria["pacientes"])
        return True
    return False

# === TURNOS E HISTORIAL ===
def _gen_id(lista):
    max_id = 0
    for item in lista:
        if item["id"] > max_id:
            max_id = item["id"]
    return max_id + 1

def agregar_turno(data):
    data["id"] = _gen_id(_memoria["turnos"])
    _memoria["turnos"].append(data)
    guardar_archivo("turnos", _memoria["turnos"])
    return data["id"]

def listar_turnos():
    return _memoria["turnos"]

def cancelar_turno(id_turno):
    turno = None
    for t in _memoria["turnos"]:
        if t["id"] == id_turno:
            turno = t
            break
    
    if turno:
        turno["estado"] = "Cancelado"
        guardar_archivo("turnos", _memoria["turnos"])
        return True
    return False

def buscar_turnos_por_paciente(dni):
    res = []
    for t in _memoria["turnos"]:
        if t["paciente_dni"] == dni and t["estado"] == "Confirmado":
            res.append(t)
    return res

def buscar_turnos_por_medico(dni):
    res = []
    for t in _memoria["turnos"]:
        if t["medico_dni"] == dni and t["estado"] == "Confirmado":
            res.append(t)
    return res

def agregar_historial(m_dni, p_dni, t_id, fecha, est="Confirmado"):
    nuevo = {
        "id": _gen_id(_memoria["historial"]), 
        "medico_dni": m_dni, 
        "paciente_dni": p_dni, 
        "turno_id": t_id, 
        "fecha": fecha, 
        "estado": est
    }
    _memoria["historial"].append(nuevo)
    guardar_archivo("historial", _memoria["historial"])

def obtener_historial_por_medico(dni):
    res = []
    for h in _memoria["historial"]:
        if h["medico_dni"] == dni:
            res.append(h)
    return res

def actualizar_estado_historial(t_id, est):
    hist = None
    for h in _memoria["historial"]:
        if h["turno_id"] == t_id:
            hist = h
            break
            
    if hist:
        hist["estado"] = est
        guardar_archivo("historial", _memoria["historial"])

def comparar_medicos_historial(dni1, dni2):
    h1 = obtener_historial_por_medico(dni1)
    h2 = obtener_historial_por_medico(dni2)
    
    # Usamos sets para facilitar la intersección, 
    s1 = set()
    for x in h1:
        if x["estado"] == "Confirmado":
            s1.add(x["paciente_dni"])
            
    s2 = set()
    for x in h2:
        if x["estado"] == "Confirmado":
            s2.add(x["paciente_dni"])
            
    return {
        "comunes": s1 & s2,
        "solo_medico1": s1 - s2,
        "solo_medico2": s2 - s1
    }
datos = _memoria