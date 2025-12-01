import gestor_datos
import os
from pathlib import Path 

# Obtenemos la ruta base usando OS (como pediste)
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_TEST = os.path.join(DIRECTORIO_BASE, "data_test")

if not os.path.exists(RUTA_TEST):
    os.makedirs(RUTA_TEST)
    
# Aunque usamos os.path.join, envolvemos el resultado en Path()
# porque tu gestor_datos.py usa .exists() y necesita objetos Path.
gestor_datos.FILES = {
    "personas": Path(os.path.join(RUTA_TEST, "test_personas.json")),
    "medicos": Path(os.path.join(RUTA_TEST, "test_medicos.json")),
    "pacientes": Path(os.path.join(RUTA_TEST, "test_pacientes.json")),
    "turnos": Path(os.path.join(RUTA_TEST, "test_turnos.json")),
    "historial": Path(os.path.join(RUTA_TEST, "test_historial.json")),
    "especialidades": Path(os.path.join(RUTA_TEST, "test_especialidades.json")),
    "obras_sociales": Path(os.path.join(RUTA_TEST, "test_obras_sociales.json")),
}

# Inicializamos
gestor_datos.inicializar_storage()

# ---------------------------------------------------------------

def limpiar_memoria_test():
    gestor_datos._memoria = {
        "personas": [], "medicos": [], "pacientes": [], 
        "turnos": [], "historial": [], 
        "especialidades": [], "obras_sociales": []
    }
    for k, v in gestor_datos._memoria.items():
        if k in ["especialidades", "obras_sociales"]: continue
        gestor_datos.guardar_archivo(k, v)

# --- TESTS UNITARIOS ---
def test_agregar_medico():
    limpiar_memoria_test()
    
    medico_prueba = {
        "DNI": 20500100,
        "Nombre": "Dr. House Test",
        "Fecha de Nacimiento": [1975, 5, 20],
        "Especialidad": "Diagnóstico",
        "Horarios": {"Lunes": [9, 18]},
        "Estado": "Disponible"
    }
    
    gestor_datos.agregar_medico(medico_prueba)
    
    resultado = gestor_datos.obtener_medico(20500100)
    assert resultado is not None
    assert resultado["Nombre"] == "Dr. House Test"

def test_agregar_paciente():
    limpiar_memoria_test()
    
    paciente_prueba = {
        "DNI": 30100200,
        "Nombre": "Paciente Test",
        "Fecha de Nacimiento": [1990, 1, 1],
        "Obra Social": "OSDE"
    }
    
    gestor_datos.agregar_paciente(paciente_prueba)
    
    resultado = gestor_datos.obtener_paciente(30100200)
    assert resultado is not None
    assert resultado["Nombre"] == "Paciente Test"

def test_integridad_medico_paciente():
    limpiar_memoria_test()
    dni = 20500100
    
    gestor_datos.agregar_medico({
        "DNI": dni, "Nombre": "Dra. Grey Test", "Fecha de Nacimiento": [1980, 1, 1],
        "Especialidad": "Cirugía", "Horarios": {}
    })
    
    gestor_datos.agregar_paciente({
        "DNI": dni, "Nombre": "Dra. Grey Test", "Fecha de Nacimiento": [1980, 1, 1],
        "Obra Social": "Hospital"
    })
    
    assert gestor_datos.obtener_medico(dni) is not None
    assert gestor_datos.obtener_paciente(dni) is not None

def test_agendar_turno():
    limpiar_memoria_test()
    
    nt = {
        "medico_dni": 20500100, "paciente_dni": 30100200,
        "fecha": (2025, 10, 1), "hora": (10, 0), "estado": "Confirmado"
    }
    
    id_gen = gestor_datos.agregar_turno(nt)
    assert id_gen > 0
    
    todos = gestor_datos.listar_turnos()
    encontrado = False
    for t in todos:
        if t["id"] == id_gen:
            encontrado = True
            break
    assert encontrado == True

def test_eliminar_medico():
    limpiar_memoria_test()
    
    medico = {
        "DNI": 11111111, "Nombre": "Borrar", 
        "Fecha de Nacimiento": [1990, 1, 1], "Especialidad": "Test", "Horarios": {}
    }
    gestor_datos.agregar_medico(medico)
    
    assert gestor_datos.obtener_medico(11111111) is not None
    
    gestor_datos.eliminar_medico(11111111)
    
    assert gestor_datos.obtener_medico(11111111) is None

"""
def test_falla_porque_no_existe():
    #Este test FALLARÁ porque buscamos un DNI que no existe y afirmamos que el sistema debería encontrarlo.
    limpiar_memoria_test()
    
    # Intentamos buscar un DNI inexistente
    resultado = gestor_datos.obtener_medico(99999999)

    # El resultado será None, pero el test exige que NO sea None.
    assert resultado is not None

def test_falla_por_nombre_incorrecto():
    
    #Simula que esperamos un resultado (Wilson) pero el sistema tiene otro (House).
    limpiar_memoria_test()
    medico_house = {
        "DNI": 12345678,
        "Nombre": "Dr. House", # Nombre correcto en el sistema
        "Fecha de Nacimiento": [1960, 1, 1],
        "Especialidad": "Diagnóstico",
        "Horarios": {},
        "Estado": "Disponible"
    }
    gestor_datos.agregar_medico(medico_house)
    recuperado = gestor_datos.obtener_medico(12345678)
    
    assert recuperado["Nombre"] == "Dr. Wilson" # Aca falla porque el nombre no coincide 
"""