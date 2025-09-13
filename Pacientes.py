import os
from Diccionarios import pacientes



def mostrarLista():
    for paciente in pacientes:
        for dni,datos in paciente.items():
            print("\n")
            print(f"DNI:{dni} | Nombre:{datos['Nombre']} | Edad:{datos['Edad']} | Obra Social:{datos['Obra Social']}")

    input("\nPresione Enter para continuar...")
    os.system('cls')
    return

def agregarPaciente():
    while True:
        band = True
        dni = int(input("Ingresar Numero de DNI: "))
        for diccionario in pacientes:
            for identificacion,datos in diccionario.items():
                if dni == identificacion:
                    band = False

        if band == True:
            pacientes.append({dni:
            {"Nombre": input("ingresar el nombre: "),
            "Edad" : input("ingresar edad: "),
            "Obra Social" : input("ingresar Obra Social: ")}
            })
            print("El paciente se agrego correctamente")
            input("\n presione enter para continuar")
            break

        else:    
            print("El paciente ya esta en la lista")
            input("\n presione enter para continuar")
            os.system('cls')

    mostrarLista()
    return

def eliminarPaciente():
    while True:
        band = True
        dni = int(input("Ingresar Numero de DNI: "))
        for diccionario in pacientes:
            for identificacion,datos in diccionario.items():
                if dni == identificacion:
                    band = False
        
        if band == False:
            for diccionario in range(len(pacientes)):
                    for identificacion,datos in pacientes[diccionario].items():
                        if dni == identificacion:
                            del pacientes[diccionario]
                            print(f"El paciente {datos['Nombre']} se elimino correctamente de la lista")
                            input("\n presione enter para continuar")
                            mostrarLista()
                            return
                
        print("El paciente no existe en la lista")
        input("\n presione enter para continuar")
        os.system('cls')
                    

def modificarPaciente():
    while True:
        dni = int(input("Ingresar Numero de DNI: "))
        for diccionario in pacientes:
            for identificacion,datos in diccionario.items():
                if dni == identificacion:
                    aux = datos
                    while True:
                        edad = int(input("Ingresar la edad: "))
                        if edad < 1:
                            print("La edad es incorrecta")
                        else:
                            nombre = input("Ingresar el Nombre: ")
                            obraSocial = input("Ingresar la Obra Social: ")
                            aux["Nombre"] = nombre
                            aux["Edad"] = edad
                            aux["Obra Social"] = obraSocial
                            print(f"El paciente {datos['Nombre']} se le han modificado sus datos correctamente")
                            input("\n presione enter para continuar")
                            mostrarLista()
                            return
                        
        print("El paciente no existe en la lista")
        input("\n presione enter para continuar")
        os.system('cls')



def main():
    ...
main()