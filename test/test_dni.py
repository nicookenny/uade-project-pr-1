import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch
from FuncionesGenerales import CargarDNI

def test_dni_valido():
    with patch('builtins.input', return_value='12345678'):
        resultado = CargarDNI("usuario")
        assert resultado == 12345678

def test_dni_invalido_hasta_valido():
    with patch('builtins.input', side_effect=['abc', '123', '87654321']):
        resultado = CargarDNI("usuario")
        assert resultado == 87654321