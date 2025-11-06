from functools import reduce
import json
import re

# Convierte los datos de los archivos en diccionario
def convertirDiccionario(datos):
    diccionario = {
        "Año": datos[0],
        "Precio": datos[1],
        "Km": datos[2],
        "Ubicacion": datos[3],
        "Estado": datos[4]
    }
    return diccionario

#Valida si el precio es de tipo entero o si tiene caracteres especiales
def VerificarPrecio(precio):
    patronPrecio = r"^\d+(\.\d{1,2})?$"
    if re.match(patronPrecio, str(precio)):
        return precio
    else:
        resultado = re.findall(r"\d+(?:[.,]\d+)*", precio)
        resultados_limpios = [n.replace(".", "").replace(",", "") for n in resultado]
        return resultados_limpios[0]
    

#Importa los datos del archivo jason 
def importarDatosJSON():
    try:
        lista = []
        archivo = open("C:\\Users\\Koichi\\Documents\\Programacion 1\\TrabajoIntegrador\\tasadores.json",mode="r",encoding="utf-8")
        lineas = archivo.read()
        archivo.close()
        vehiculos = json.loads(lineas)
        for autos in vehiculos:
            diccionario = {}
            for datos,info in autos.items():
                informacion = str(info).capitalize()
                dato = str(datos).capitalize()
                diccionario[dato] = informacion
                if datos == "precio":
                     diccionario[dato] = VerificarPrecio(info)
            lista.append(diccionario)
                    
        return lista

    except:
        print("No se puede abrir el archivo")


#Importa los datos del archivo csv
def importarDatosCSV(ruta):
    try:
        lista = []
        diccionario = {}
        archivo = open(ruta,mode="r",encoding="utf-8")
        for linea in archivo:
            if "," in linea:
                linea = linea.strip()
                linea = linea.split(",")
                palabras = [letra.capitalize() for letra in linea]
                filtro = palabras[2::]
                convertir = convertirDiccionario(filtro)
                suma = palabras[0]+palabras[1]
                if not "MarcaModelo" in suma:
                    diccionario[suma] = convertir
                    
        lista.append(diccionario)
        archivo.close()
        return lista
    
    except:
        print("No se puede abrir el archivo")


#Importa los datos del archivo txt
def importarDatosTXT():
    try:
        lista = []
        diccionario = {}
        archivo = open("C:\\Users\\Koichi\\Documents\\Programacion 1\\TrabajoIntegrador\\aseguradoras.txt",mode="r",encoding="utf-8")
        for linea in archivo:
            linea = linea.strip()
            linea = linea.split("|")
            palabras = [letra.capitalize() for letra in linea]
            palabrasSlice = palabras[2::]
            convertir = convertirDiccionario(palabrasSlice)
            suma = palabras[0] + palabras[1]
            if not "MarcaModelo" in suma:
                diccionario[suma] = convertir

        for datos,info in diccionario.items():
            info["Precio"] = VerificarPrecio(info["Precio"])
    
        lista.append(diccionario)
        archivo.close()

        return lista
    
    except:
        print("No se puede abrir el archivo")


#Junta toda la informacion filtrada de cada archivo y los carga en una archivo json
def cargarArchivo(txt, csv1,csv2, jason):
    archivo = open("C:\\Users\\Koichi\\Documents\\Programacion 1\\TrabajoIntegrador\\cargaArchivos.json", mode="w", encoding="utf-8")
    
    datos = {
        "txt": txt,
        "csv1": csv1,
        "csv2": csv2,
        "json": jason
    }
    
    json.dump(datos, archivo, ensure_ascii=False, indent=4)
    archivo.close()
    return


#Con los datos filtrados del json busca por "Estado" cuantos hay de cada uno
def contarVehiculosPorEstado(txt, csv1, csv2, json):
    # Unimos todas las listas
    datos_totales = txt + csv1 + csv2

    estados = []

   
    for grupo in datos_totales:
        for auto, info in grupo.items():
            if "Estado" in info:
                estados.append(str(info["Estado"]).capitalize())

 
    for vehiculo in json:
        if "Estado" in vehiculo:
            estados.append(str(vehiculo["Estado"]).capitalize())

    # Contamos los estados con reduce
    conteo = reduce(
        lambda acc, est: {**acc, est: acc.get(est, 0) + 1},
        estados,
        {}
    )
    for estado,cantidad in conteo.items():
        print(f'Autos con Estado: {estado}, Cantidad: {cantidad}')
    return 


ruta1 = "C:\\Users\\Koichi\\Documents\\Programacion 1\\TrabajoIntegrador\\portales.txt"
ruta2 = "C:\\Users\\Koichi\\Documents\\Programacion 1\\TrabajoIntegrador\\auto_matriz.txt"

txt = importarDatosTXT()
csv1 = importarDatosCSV(ruta1)
csv2 = importarDatosCSV(ruta2)
jason = importarDatosJSON()
cargarArchivo(txt,csv1,csv2,jason)
contarVehiculosPorEstado(txt,csv1,csv2,jason)




