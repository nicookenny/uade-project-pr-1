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

_datos = {
    "medicos": [],
    "pacientes": [],
    "turnos": [],
    "historial": [],
}


def inicializar_storage():
    """Crea el directorio data/ y archivos JSON si no existen"""
    STORAGE_DIR.mkdir(exist_ok=True)

    datos_archivos = ["medicos", "pacientes", "turnos", "historial"]
    for nombre in datos_archivos:
        ruta = FILES[nombre]
        if not ruta.exists():
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    for nombre in ["especialidades", "obras_sociales"]:
        ruta = FILES[nombre]
        if not ruta.exists():
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(REFERENCE_DATA[nombre], f, ensure_ascii=False, indent=2)


def cargar_datos():
    """Carga todos los datos desde los archivos JSON"""
    datos = {
        "medicos": [],
        "pacientes": [],
        "turnos": [],
        "historial": [],
        "especialidades": [],
        "obras_sociales": [],
    }

    for clave, ruta in FILES.items():
        try:
            if ruta.exists():
                with open(ruta, "r", encoding="utf-8") as f:
                    datos[clave] = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: archivo {ruta} corrupto, se ignorará")
        except Exception as e:
            print(f"Error cargando {ruta}: {e}")

    return datos


def _guardar_archivo(nombre, datos):
    """Helper para guardar un archivo JSON"""
    ruta = FILES[nombre]
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando {nombre}: {e}")


class _PacientesStorage:
    """CRUD operations for Pacientes"""

    def agregar(self, paciente_data):
        """Agrega un nuevo paciente"""
        _datos["pacientes"].append(paciente_data)
        _guardar_archivo("pacientes", _datos["pacientes"])

    def eliminar(self, dni):
        """Elimina un paciente por DNI"""
        for i, p in enumerate(_datos["pacientes"]):
            if p["DNI"] == dni:
                del _datos["pacientes"][i]
                _guardar_archivo("pacientes", _datos["pacientes"])
                return True
        return False

    def modificar(self, dni, new_data):
        """Modifica datos de un paciente"""
        for p in _datos["pacientes"]:
            if p["DNI"] == dni:
                p.update(new_data)
                _guardar_archivo("pacientes", _datos["pacientes"])
                return True
        return False

    def obtener(self, dni):
        """Obtiene un paciente por DNI"""
        for i, p in enumerate(_datos["pacientes"]):
            if p["DNI"] == dni:
                return (i, p)
        return None

    def listar(self):
        """Lista todos los pacientes"""
        return _datos["pacientes"]


class _MedicosStorage:
    """CRUD operations for Medicos"""

    def agregar(self, medico_data):
        """Agrega un nuevo médico"""
        _datos["medicos"].append(medico_data)
        _guardar_archivo("medicos", _datos["medicos"])

    def eliminar(self, dni):
        """Elimina un médico por DNI"""
        for i, m in enumerate(_datos["medicos"]):
            if m["DNI"] == dni:
                del _datos["medicos"][i]
                _guardar_archivo("medicos", _datos["medicos"])
                return True
        return False

    def modificar(self, dni, new_data):
        """Modifica datos de un médico"""
        for m in _datos["medicos"]:
            if m["DNI"] == dni:
                m.update(new_data)
                _guardar_archivo("medicos", _datos["medicos"])
                return True
        return False

    def obtener(self, dni):
        """Obtiene un médico por DNI"""
        for m in _datos["medicos"]:
            if m["DNI"] == dni:
                return m
        return None

    def listar(self):
        """Lista todos los médicos"""
        return _datos["medicos"]


class _TurnosStorage:
    """CRUD operations for Turnos"""

    def _generar_id(self):
        """Genera un ID único para turnos"""
        if not _datos["turnos"]:
            return 1
        return max(t["id"] for t in _datos["turnos"]) + 1

    def agregar(self, turno_data):
        """Agrega un nuevo turno y retorna el ID"""
        if "id" not in turno_data:
            turno_data["id"] = self._generar_id()
        _datos["turnos"].append(turno_data)
        _guardar_archivo("turnos", _datos["turnos"])
        return turno_data["id"]

    def cancelar(self, turno_id):
        """Cancela un turno"""
        for t in _datos["turnos"]:
            if t["id"] == turno_id:
                t["estado"] = "Cancelado"
                _guardar_archivo("turnos", _datos["turnos"])
                return True
        return False

    def obtener(self, turno_id):
        """Obtiene un turno por ID"""
        for t in _datos["turnos"]:
            if t["id"] == turno_id:
                return t
        return None

    def listar(self):
        """Lista todos los turnos"""
        return _datos["turnos"]

    def buscar_por_paciente(self, paciente_dni):
        """Obtiene turnos de un paciente"""
        return [
            t
            for t in _datos["turnos"]
            if t["paciente_dni"] == paciente_dni and t["estado"] == "Confirmado"
        ]

    def buscar_por_medico(self, medico_dni):
        """Obtiene turnos de un médico"""
        return [
            t
            for t in _datos["turnos"]
            if t["medico_dni"] == medico_dni and t["estado"] == "Confirmado"
        ]


class _HistorialStorage:
    """CRUD operations for Historial"""

    def _generar_id(self):
        """Genera un ID único para el historial"""
        if not _datos["historial"]:
            return 1
        return max(h["id"] for h in _datos["historial"]) + 1

    def agregar(self, medico_dni, paciente_dni, turno_id, fecha, estado="Confirmado"):
        """Agrega una nueva entrada al historial"""
        nueva_entrada = {
            "id": self._generar_id(),
            "medico_dni": medico_dni,
            "paciente_dni": paciente_dni,
            "turno_id": turno_id,
            "fecha": fecha,
            "estado": estado,
        }
        _datos["historial"].append(nueva_entrada)
        _guardar_archivo("historial", _datos["historial"])
        return nueva_entrada["id"]

    def actualizar_estado(self, turno_id, nuevo_estado):
        """Actualiza el estado de un historial"""
        for h in _datos["historial"]:
            if h["turno_id"] == turno_id:
                h["estado"] = nuevo_estado
                _guardar_archivo("historial", _datos["historial"])
                return True
        return False

    def obtener_por_paciente(self, paciente_dni):
        """Obtiene historial de un paciente"""
        return [h for h in _datos["historial"] if h["paciente_dni"] == paciente_dni]

    def obtener_por_medico(self, medico_dni):
        """Obtiene historial de un médico"""
        return [h for h in _datos["historial"] if h["medico_dni"] == medico_dni]

    def comparar_medicos(self, dni1, dni2):
        """Compara historial entre dos médicos"""
        historial1 = self.obtener_por_medico(dni1)
        historial2 = self.obtener_por_medico(dni2)

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

    def eliminar_por_medico(self, medico_dni):
        """Elimina historial de un médico"""
        _datos["historial"] = [
            h for h in _datos["historial"] if h["medico_dni"] != medico_dni
        ]
        _guardar_archivo("historial", _datos["historial"])

    def listar(self):
        """Lista todo el historial"""
        return _datos["historial"]


Pacientes = _PacientesStorage()
Medicos = _MedicosStorage()
Turnos = _TurnosStorage()
Historial = _HistorialStorage()

especialidades_medicas = tuple(REFERENCE_DATA["especialidades"])
obras_y_prepagas_arg = tuple(REFERENCE_DATA["obras_sociales"])

inicializar_storage()
datos_cargados = cargar_datos()
_datos["medicos"] = datos_cargados["medicos"]
_datos["pacientes"] = datos_cargados["pacientes"]
_datos["turnos"] = datos_cargados["turnos"]
_datos["historial"] = datos_cargados["historial"]
