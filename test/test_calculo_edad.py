import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date
from FuncionesGenerales import CalculoEdad

def test_calculo_edad_cumple_este_anio():
    # Ejemplo: si nació el 1 de enero de 2000 y hoy es 2025, debería tener 25
    hoy = date.today()
    fecha_nac = (2000, 1, 1)
    edad = CalculoEdad(fecha_nac)
    assert edad == hoy.year - 2000

def test_calculo_edad_no_cumplio_este_anio():
    # Ejemplo: si nació el 31 de diciembre de 2000 y hoy es 2025 pero antes de su cumpleaños
    hoy = date.today()

    # creamos una fecha posterior al día actual, dentro del mismo año
    fecha_nac = (2000, hoy.month + 1 if hoy.month < 12 else 1, hoy.day)
    edad = CalculoEdad(fecha_nac)

    # en este caso, deberia ser un año menos
    assert edad == hoy.year - 2000 - 1