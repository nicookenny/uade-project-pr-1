from datetime import datetime
import re


def validarUbicacion(ubicacion):
    if not isinstance(ubicacion, str) or not ubicacion.strip():
        return False
    return True


def validarEstado(estado):
    if not isinstance(estado, str) or not estado.strip():
        return False
    return True


def validarAño(año):
    try:
        año_limpio = int(str(año).strip())
        if año_limpio < 1900 or año_limpio > datetime.now().year:
            return None
        return año_limpio
    except (ValueError, TypeError):
        return None


def validarKm(strKm):
    if strKm is None:
        return None
    try:
        km_limpio = str(strKm).strip().replace(".", "").replace(",", "")
        km = int(km_limpio)
        if km < 0:
            return None
        return km
    except ValueError:
        return None


def validarPrecio(precio):
    precio_str = str(precio).strip()
    precio_str = re.sub(r"[OO](?=\d)", "0", precio_str)
    precio_str = re.sub(r"[^\d.,]", "", precio_str)

    patronPrecio = r"^\d+(?:[.,]\d+)*$"
    if re.match(patronPrecio, precio_str):
        precio_limpio = precio_str.replace(".", "").replace(",", "")
        return int(precio_limpio)
    else:
        resultado = re.findall(r"\d+(?:[.,]\d+)*", precio_str)
        if resultado:
            precio_limpio = resultado[0].replace(".", "").replace(",", "")
            return int(precio_limpio)
        return None
