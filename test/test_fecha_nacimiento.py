import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch
from FuncionesGenerales import CargarFechaDeNacimiento

def test_fecha_valida():
    # Usuario ingresa una fecha correcta
    with patch('builtins.input', return_value='01/01/2000'):
        resultado = CargarFechaDeNacimiento()
        assert resultado == (2000, 1, 1)

def test_fecha_invalida_hasta_valida():
    # El usuario ingresa primero algo mal, luego una fecha válida
    entradas = ['32/01/2000', '15/13/1999', '01/01/2000']
    with patch('builtins.input', side_effect=entradas):
        resultado = CargarFechaDeNacimiento()
        assert resultado == (2000, 1, 1)

def test_fecha_futura():
    # El usuario ingresa una fecha en el futuro, luego una válida
    from datetime import date
    anio_futuro = date.today().year + 1
    entradas = [f'01/01/{anio_futuro}', '01/01/2000']
    with patch('builtins.input', side_effect=entradas):
        resultado = CargarFechaDeNacimiento()
        assert resultado == (2000, 1, 1)