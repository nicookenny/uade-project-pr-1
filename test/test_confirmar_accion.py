import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch
from FuncionesGenerales import confirmar_accion

def test_confirmar_accion_si_confirma():
    # Simula que el usuario ingresa "s"
    with patch("builtins.input", return_value="s"):
        resultado = confirmar_accion("¿Desea continuar?")
    assert resultado is True


def test_confirmar_accion_no_confirma():
    # Simula que el usuario ingresa "n"
    with patch("builtins.input", return_value="n"), \
         patch("FuncionesGenerales.pausar"), \
         patch("FuncionesGenerales.limpiar_pantalla"), \
         patch("builtins.print") as mock_print:

        resultado = confirmar_accion("¿Desea continuar?")
    
    # Verifica que devolvió False
    assert resultado is False
    # Verifica que imprimió el mensaje de cancelación
    mock_print.assert_any_call("Acción cancelada por el usuario.")