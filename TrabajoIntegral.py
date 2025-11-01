import json
import re

def VerificarPrecio(precio):
    patronPrecio = r"^\d+(\.\d{1,2})?$"
    if re.match(patronPrecio, str(precio)):
        return precio
    else:
        return -1

def importarDatosJSON():
    try:
        archivo = open("C:\\Users\\Koichi\\Documents\\Programacion 1\\tasadores.json",mode="r",encoding="utf-8")
        lineas = archivo.read()
        archivo.close()
        vehiculos = json.loads(lineas)
        for autos in vehiculos:
            for datos,info in autos.items():
                print(info)
                if datos == "precio":
                    e = VerificarPrecio(info)
                    print(e)
        return lista

    except:
        print("No se puede abrir el archivo")



def importarDatosCSV():
    lista = []
    diccionario = {}
    archivo = open("C:\\Users\\Koichi\\Documents\\Programacion 1\\formatoCSV.txt",mode="r",encoding="utf-8")
    for linea in archivo:
        if "," in linea:
            linea = linea.strip()
            linea = linea.split(",")
            palabras = [letra.capitalize() for letra in linea]
            compresion = palabras[2::]
            suma = palabras[0]+palabras[1]
            if not "MarcaModelo" in suma:
                diccionario[suma] = compresion
    
    lista.append(diccionario)
    archivo.close()
    return lista

def importarDatosTXT():
    lista = []
    diccionario = {}
    archivo = open("C:\\Users\Koichi\\Documents\\Programacion 1\\aseguradoras.txt",mode="r",encoding="utf-8")
    for linea in archivo:
        linea = linea.strip()
        linea = linea.split("|")
        palabras = [letra.capitalize() for letra in linea]
        compresion = palabras[2::]
        suma = palabras[0] + palabras[1]
        if not "MarcaModelo" in suma:
            diccionario[suma] = compresion

    for datos,info in diccionario.items():
        print(info)
        e = VerificarPrecio(info[1])
        print(e)
        
    
    lista.append(diccionario)
    print(lista)
    archivo.close()

    return lista

def cargarArchivo(txt,csv):
    archivo = open("C:\\Users\\Koichi\\Documents\\Programacion 1\\cargaArchivos.json",mode="a", encoding="utf-8")
    json.dump(txt, archivo, ensure_ascii=False, indent=4)
    json.dump(csv, archivo, ensure_ascii=False, indent=4)

txt = importarDatosTXT()
csv = importarDatosCSV()
cargarArchivo(txt,csv)

