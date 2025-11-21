import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch
from FuncionesGenerales import CargarNombre

def test_nombre_valido():
    # El usuario ingresa un nombre correcto a la primera
    with patch('builtins.input', return_value='Juan Perez'):
        resultado = CargarNombre()
        assert resultado == 'Juan Perez'

def test_nombre_invalido_hasta_valido():
    # El usuario ingresa primero algo incorrecto, luego algo correcto
    entradas = ['J', 'Juan@123', 'Ana Maria']
    with patch('builtins.input', side_effect=entradas):
        resultado = CargarNombre()
        assert resultado == 'Ana Maria'

def test_nombre_con_caracteres_permitidos():
    # El usuario usa apóstrofe y guion, que deben ser válidos
    with patch('builtins.input', return_value="Maria O'Connor"):
        resultado = CargarNombre()
        assert resultado == "Maria O'Connor"