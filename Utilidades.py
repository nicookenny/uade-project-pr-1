from functools import reduce
import json
import os
import re


def convertirLineaDict(linea):
    diccionario = {}
    diccionario["marca"] = linea[0]
    diccionario["modelo"] = linea[1]
    diccionario["año"] = linea[2]
    diccionario["precio"] = linea[3]
    diccionario["km"] = linea[4]
    diccionario["ubicacion"] = linea[5]
    diccionario["estado"] = linea[6]
    return diccionario


def contarEstado(datos, estado):
    total = reduce(
        lambda acc, auto: acc
        + (1 if auto.get("estado", "").capitalize() == estado.capitalize() else 0),
        datos,
        0,
    )
    return total


def esHeader(linea):
    campos_esperados = {"marca", "modelo", "año", "precio", "km", "ubicacion", "estado"}
    campos_linea = {campo.strip().lower() for campo in linea}
    return campos_linea == campos_esperados


def eliminarDuplicados(autos):
    vistos = set()
    resultado = []

    for auto in autos:
        clave = (
            auto.get("marca", "").lower(),
            auto.get("modelo", "").lower(),
            auto.get("año"),
            auto.get("precio"),
            auto.get("km"),
            auto.get("ubicacion", "").lower(),
            auto.get("estado", "").lower(),
        )

        if clave not in vistos:
            vistos.add(clave)
            resultado.append(auto)

    return resultado


def limpiar_precio(precio_raw: str) -> str:
    s = re.sub(r"[^\d,\.]", "", precio_raw)

    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    else:
        if "," in s:
            s = s.replace(".", "").replace(",", ".")
        else:
            pass

    return s


def limpiarPrecios(listaAutos):
    resultado = []

    for auto in listaAutos:
        copia = auto.copy()
        if "precio" in copia:
            precio_raw = str(copia["precio"]).strip()
            precio_limpio = limpiar_precio(precio_raw)

            if precio_limpio:
                try:
                    copia["precio"] = int(precio_limpio)
                except ValueError:
                    copia["precio"] = -1
            else:
                copia["precio"] = -1

        resultado.append(copia)

    return resultado


def exportarArchivo(autos, nombre_archivo):
    try:
        raiz = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(raiz, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(autos, archivo, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error al exportar archivo: {e}")
        return False
