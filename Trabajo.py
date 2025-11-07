import json
import os
import re
from datetime import datetime
from functools import reduce
import Utilidades
import Validaciones
from pathlib import Path


def validarAuto(auto):
    # Verifica si el auto es un diccionario
    if not isinstance(auto, dict):
        return False

    # Verifica si el auto tiene las claves requeridas
    claves_requeridas = {"año", "precio", "km", "ubicacion", "estado"}
    if not all(clave in auto for clave in claves_requeridas):
        return False

    # Verifica y sanitiza los campos del auto
    try:
        año = Validaciones.validarAño(auto["año"])
        if año is None:
            return False
        auto["año"] = año

        km = Validaciones.validarKm(auto["km"])
        if km is None:
            return False
        auto["km"] = km

        precio = Validaciones.validarPrecio(auto["precio"])
        if precio is None or precio <= 0:
            return False
        auto["precio"] = precio

        if not Validaciones.validarUbicacion(auto["ubicacion"]):
            return False
        auto["ubicacion"] = str(auto["ubicacion"]).strip().upper()

        if not Validaciones.validarEstado(auto["estado"]):
            return False
        auto["estado"] = str(auto["estado"]).strip().upper()

        return True
    except Exception as e:
        print(f"Error al validar el auto: {e}")
        return False


def procesarArchivoJSON(ruta):
    autos = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.read()
            datos = json.loads(lineas)
            for auto in datos:
                if validarAuto(auto):
                    autos.append(auto)
                else:
                    print(f"Error al procesar el auto: {auto}")
    except FileNotFoundError:
        print("No se puede abrir el archivo")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
    return autos


def procesarArchivoTXT(ruta):
    autos = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        if not lineas:
            return autos

        primera_linea = lineas[0].strip()
        separador = "|" if "|" in primera_linea else ","

        primera_split = primera_linea.split(separador)
        es_header = Utilidades.esHeader(primera_split)

        inicio = 1 if es_header else 0

        for i in range(inicio, len(lineas)):
            linea = lineas[i].strip()
            if not linea:
                continue
            linea = linea.split(separador)
            auto_resultado = Utilidades.convertirLineaDict(linea)
            if validarAuto(auto_resultado):
                autos.append(auto_resultado)
            else:
                print(f"Error al procesar el auto: {auto_resultado}")
    except FileNotFoundError:
        print("No se puede abrir el archivo")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
    return autos


def procesarArchivoCSV(ruta):
    autos = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                linea = linea.split(",")
                auto_resultado = Utilidades.convertirLineaDict(linea)
                if validarAuto(auto_resultado):
                    autos.append(auto_resultado)
                else:
                    print(f"Error al procesar el auto: {auto_resultado}")
    except FileNotFoundError:
        print("No se puede abrir el archivo")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
    return autos


def importarDatos(rutasArchivos):
    autos = []

    for ruta in rutasArchivos:
        path = Path(ruta)
        resultado = None
        if path.suffix == ".json":
            resultado = procesarArchivoJSON(ruta)
        elif path.suffix == ".csv":
            resultado = procesarArchivoCSV(ruta)
        elif path.suffix == ".txt":
            resultado = procesarArchivoTXT(ruta)
        else:
            continue

        if resultado:
            autos.extend(resultado)

    autos = Utilidades.limpiarPrecios(autos)
    return Utilidades.eliminarDuplicados(autos)


# use lib to get the root of the project
root = os.path.dirname(os.path.abspath(__file__))

rutas = []

rutas.append(os.path.join(root, "tasadores.json"))
rutas.append(os.path.join(root, "auto_matriz.txt"))
rutas.append(os.path.join(root, "aseguradoras.txt"))
rutas.append(os.path.join(root, "portales.csv"))

autos = importarDatos(rutas)
if Utilidades.exportarArchivo(autos, "unificados.json"):
    print(f"Archivo exportado exitosamente: unificados.json")
    print(f"Total de autos procesados: {len(autos)}")
else:
    print("Error al exportar el archivo")

print(f"Total de autos excelentes: {Utilidades.contarEstado(autos, 'excelente')}")
print(f"Total de autos buenos: {Utilidades.contarEstado(autos, 'bueno')}")
print(f"Total de autos regulares: {Utilidades.contarEstado(autos, 'regular')}")
print(f"Total de autos malos: {Utilidades.contarEstado(autos, 'malo')}")
print(f"Total de autos muy malos: {Utilidades.contarEstado(autos, 'muy malo')}")
print(f"Total de autos muy buenos: {Utilidades.contarEstado(autos, 'muy bueno')}")
print(
    f"Total de autos muy excelentes: {Utilidades.contarEstado(autos, 'muy excelente')}"
)
print(f"Total de autos muy buenos: {Utilidades.contarEstado(autos, 'muy bueno')}")
