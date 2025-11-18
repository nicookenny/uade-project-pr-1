import json
from pathlib import Path

STORAGE_DIR = Path(__file__).parent / "data"
FILES = {
    "medicos": STORAGE_DIR / "medicos.json",
    "pacientes": STORAGE_DIR / "pacientes.json",
    "turnos": STORAGE_DIR / "turnos.json",
    "historial": STORAGE_DIR / "historial.json",
    "especialidades": STORAGE_DIR / "especialidades.json",
    "obras_sociales": STORAGE_DIR / "obras_sociales.json",
}

REFERENCE_DATA = {
    "especialidades": [
        "Alergología",
        "Anestesiología",
        "Cardiología",
        "Cirugía General",
        "Cirugía Cardiovascular",
        "Cirugía Plástica y Reconstructiva",
        "Cirugía Pediátrica",
        "Cirugía Torácica",
        "Cirugía Vascular",
        "Dermatología",
        "Endocrinología",
        "Gastroenterología",
        "Geriatría",
        "Ginecología y Obstetricia",
        "Hematología",
        "Hepatología",
        "Infectología",
        "Medicina de Emergencias",
        "Medicina del Deporte",
        "Medicina Familiar y Comunitaria",
        "Medicina Física y Rehabilitación",
        "Medicina Intensiva",
        "Medicina Interna",
        "Medicina Legal y Forense",
        "Nefrología",
        "Neumología",
        "Neurología",
        "Neurocirugía",
        "Nutriología Clínica",
        "Oftalmología",
        "Oncología Médica",
        "Oncología Radioterápica",
        "Ortopedia y Traumatología",
        "Otorrinolaringología",
        "Pediatría",
        "Psiquiatría",
        "Radiología",
        "Reumatología",
        "Toxicología",
        "Urología",
    ],
    "obras_sociales": [
        "PAMI",
        "APM / OSAPM",
        "Activa Salud",
        "Andar",
        "APRES Salud",
        "APSOT / FFST",
        "ASMEPRIV",
        "Assistravel",
        "Avalian",
        "Banco Provincia (BCO. PCIA.)",
        "Bristol / Santa Cecilia",
        "C.A.S.A",
        "CEMIC",
        "CIMA",
        "Cobermed",
        "Cobertec / OS Mosaistas",
        "Colegio de Escribanos Plan Especial (OSSEG)",
        "COMEI",
        "Corporación Asistencial",
        "DASMI - Universidad de Luján",
        "Dom Centro de Reumatología",
        "Emergencias",
        "Empleados de Farmacia",
        "OSDE",
        "Swiss Medical",
        "Medicus",
        "Omint",
        "Galeno",
        "Medifé",
        "Sancor Salud",
        "Prevención Salud",
        "Premedic",
        "Salud y Bienestar",
        "Obras Sociales Unión Personal (UP)",
        "OSVARA",
        "OSIPE",
        "Obra Social del Personal de Edificios de Renta y Horizontal",
        "Obra Social de Petroleros Privados",
        "IO SFA (Instituto de Obra Social de las Fuerzas Armadas)",
    ],
}


def inicializar_storage():
    """Crea el directorio data/ y archivos JSON si no existen"""
    STORAGE_DIR.mkdir(exist_ok=True)

    # Archivos que empiezan vacíos
    datos_archivos = ["medicos", "pacientes", "turnos", "historial"]
    for nombre in datos_archivos:
        ruta = FILES[nombre]
        if not ruta.exists():
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    # Archivos que empiezan con datos de referencia
    for nombre in ["especialidades", "obras_sociales"]:
        ruta = FILES[nombre]
        if not ruta.exists():
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(REFERENCE_DATA[nombre], f, ensure_ascii=False, indent=2)

def cargar_datos():
    """Carga todos los datos desde los archivos JSON y los retorna"""
    # (Esta función es casi idéntica a la que tenías)
    datos_cargados = {}
    for clave, ruta in FILES.items():
        try:
            if ruta.exists():
                with open(ruta, "r", encoding="utf-8") as f:
                    datos_cargados[clave] = json.load(f)
            else:
                # Si falta un archivo de datos (no de referencia), carga vacío
                if clave not in REFERENCE_DATA:
                    datos_cargados[clave] = []
        except json.JSONDecodeError:
            print(f"Error: archivo {ruta} corrupto, se usará lista vacía")
            datos_cargados[clave] = []
        except Exception as e:
            print(f"Error cargando {ruta}: {e}")
            datos_cargados[clave] = []
    
    return datos_cargados

def guardar_datos(datos_para_guardar):
    """
    Toma el diccionario de datos completo y guarda las partes
    que pueden cambiar (médicos, pacientes, turnos, historial).
    """
    try:
        # Usamos el helper _guardar_un_archivo
        _guardar_un_archivo("medicos", datos_para_guardar["medicos"])
        _guardar_un_archivo("pacientes", datos_para_guardar["pacientes"])
        _guardar_un_archivo("turnos", datos_para_guardar["turnos"])
        _guardar_un_archivo("historial", datos_para_guardar["historial"])
        
    except Exception as e:
        print(f"\n[!] Error crítico al guardar los datos: {e}")

def _guardar_un_archivo(nombre, datos_lista):
    """Helper privado para guardar un solo archivo JSON"""
    ruta = FILES[nombre]
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos_lista, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # Es mejor manejar el error aquí por si un solo archivo falla
        print(f"Error guardando {nombre}: {e}")


# --- 3. CÓDIGO QUE SE EJECUTA AL INICIAR ---
inicializar_storage()

datos = cargar_datos()

# Exportamos las tuplas de referencia para conveniencia
especialidades_medicas = tuple(datos["especialidades"])
obras_y_prepagas_arg = tuple(datos["obras_sociales"])

# --- FUNCIONES AUXILIARES SIMPLES PARA ACCESO A DATOS ---

def agregar_medico(medico_data):
    datos["medicos"].append(medico_data)
    guardar_datos(datos)

def eliminar_medico(dni):
    for i, m in enumerate(datos["medicos"]):
        if m["DNI"] == dni:
            del datos["medicos"][i]
            guardar_datos(datos)
            return True
    return False

def modificar_medico(dni, new_data):
    for m in datos["medicos"]:
        if m["DNI"] == dni:
            m.update(new_data)
            guardar_datos(datos)
            return True
    return False

def obtener_medico(dni):
    for m in datos["medicos"]:
        if m["DNI"] == dni:
            return m
    return None

def listar_medicos():
    return datos["medicos"]

def agregar_paciente(paciente_data):
    datos["pacientes"].append(paciente_data)
    guardar_datos(datos)

def eliminar_paciente(dni):
    for i, p in enumerate(datos["pacientes"]):
        if p["DNI"] == dni:
            del datos["pacientes"][i]
            guardar_datos(datos)
            return True
    return False

def modificar_paciente(dni, new_data):
    for p in datos["pacientes"]:
        if p["DNI"] == dni:
            p.update(new_data)
            guardar_datos(datos)
            return True
    return False

def obtener_paciente(dni):
    for p in datos["pacientes"]:
        if p["DNI"] == dni:
            return p
    return None

def listar_pacientes():
    return datos["pacientes"]

def _generar_id_turno():
    if not datos["turnos"]:
        return 1
    return max(t["id"] for t in datos["turnos"]) + 1

def agregar_turno(turno_data):
    if "id" not in turno_data:
        turno_data["id"] = _generar_id_turno()
    datos["turnos"].append(turno_data)
    guardar_datos(datos)
    return turno_data["id"]

def cancelar_turno(turno_id):
    for t in datos["turnos"]:
        if t["id"] == turno_id:
            t["estado"] = "Cancelado"
            guardar_datos(datos)
            return True
    return False

def obtener_turno(turno_id):
    for t in datos["turnos"]:
        if t["id"] == turno_id:
            return t
    return None

def listar_turnos():
    return datos["turnos"]

def buscar_turnos_por_paciente(paciente_dni):
    return [
        t for t in datos["turnos"]
        if t["paciente_dni"] == paciente_dni and t["estado"] == "Confirmado"
    ]

def buscar_turnos_por_medico(medico_dni):
    return [
        t for t in datos["turnos"]
        if t["medico_dni"] == medico_dni and t["estado"] == "Confirmado"
    ]

def _generar_id_historial():
    if not datos["historial"]:
        return 1
    return max(h["id"] for h in datos["historial"]) + 1

def agregar_historial(medico_dni, paciente_dni, turno_id, fecha, estado="Confirmado"):
    nueva_entrada = {
        "id": _generar_id_historial(),
        "medico_dni": medico_dni,
        "paciente_dni": paciente_dni,
        "turno_id": turno_id,
        "fecha": fecha,
        "estado": estado,
    }
    datos["historial"].append(nueva_entrada)
    guardar_datos(datos)
    return nueva_entrada["id"]

def actualizar_estado_historial(turno_id, nuevo_estado):
    for h in datos["historial"]:
        if h["turno_id"] == turno_id:
            h["estado"] = nuevo_estado
            guardar_datos(datos)
            return True
    return False

def obtener_historial_por_paciente(paciente_dni):
    return [h for h in datos["historial"] if h["paciente_dni"] == paciente_dni]

def obtener_historial_por_medico(medico_dni):
    return [h for h in datos["historial"] if h["medico_dni"] == medico_dni]

def comparar_medicos_historial(dni1, dni2):
    historial1 = obtener_historial_por_medico(dni1)
    historial2 = obtener_historial_por_medico(dni2)
    
    pacientes_medico1 = {
        h["paciente_dni"] for h in historial1 if h["estado"] == "Confirmado"
    }
    pacientes_medico2 = {
        h["paciente_dni"] for h in historial2 if h["estado"] == "Confirmado"
    }
    
    return {
        "comunes": pacientes_medico1 & pacientes_medico2,
        "solo_medico1": pacientes_medico1 - pacientes_medico2,
        "solo_medico2": pacientes_medico2 - pacientes_medico1,
    }

def eliminar_historial_por_medico(medico_dni):
    datos["historial"] = [
        h for h in datos["historial"] if h["medico_dni"] != medico_dni
    ]
    guardar_datos(datos)

def listar_historial():
    return datos["historial"]