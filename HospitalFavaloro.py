import os

def mostrarLista(medicos): #Muestra el diccionario de medicos
    for medico in medicos:
        for med,datos in medico.items():
            print("\n")
            print(med,datos)
        
            
    return medicos

def agregarMedico(medico): #Agrega un medico al diccionario
    
    while True:
        for medic in medico:
            for med,datos in medic.items():
                print("\n")
                print(med,datos)
        band = True
        print()
        print("="*40)
        dni = int(input("Ingresar numero de documento: "))
        for diccionario in medico:
            for medicos,datos in diccionario.items():
                if dni == datos["DNI"][0]:
                    band = False
                    break

        
        if band == True:
            medico.append({"Medico_"+str(len(medico)+1):
            {"Nombre": input("ingresar el nombre: "),
            "Edad" : input("ingresar edad: "),
            "DNI" : (dni,),
            "Especialidad" : input("ingresar especialidad: ")}
            })
            print("El medico se agrego correctamente")
            input("\nPresione Enter para continuar...")
            
            break
        
        else:
            print("El medico ya existe")
            input("\n presione enter para continuar")
            os.system('cls')
        
    return 

def eliminarMedico(medico):#Elimina de la lista al medico
    while True:
        for medic in medico:
            for med,datos in medic.items():
                print("\n")
                print(med,datos)
        band = True
        print()
        print("="*40)
        dni = int(input("Ingresar numero de documento: "))
        for diccionario in medico:
            for medicos,datos in diccionario.items():
                if dni == datos["DNI"][0]:
                    band = False
                    break

        if band == False:
            for diccionario in range(len(medico)):
                for medicos,datos in medico[diccionario].items():
                    if dni == datos["DNI"][0]:
                        del medico[diccionario]
                        print(f'El {medicos}, {datos["Nombre"]} se elimino correctamente de la lista')
                        input("\nPresione Enter para continuar...")
                        break     
                break
            break
            
            
        
        
        else:
            print("El medico no esta en la lista")
            input("\n presione enter para continuar")
            os.system('cls')
    return

def modificarMedico(medico):#Modifica datos del medico
    while True:
        for medic in medico:
            for med,datos in medic.items():
                print("\n")
                print(med,datos)
        print()
        print("="*40)
        dni = int(input("Ingresar DNI del medico: "))

        for diccionario in medico:
            for medicos,datos in diccionario.items():
                if dni == datos["DNI"][0]:
                    while True:
                        edad = int(input("Ingresar edad: "))
                        if edad < 20:
                            print("La edad no es suficiente")
                        else:
                            nombre = input("Ingresar Nombre: ")
                            especialidad = input("Ingresar la especialidad: ")
                            datos["Nombre"] = nombre
                            datos["Edad"] = str(edad)
                            datos["Especialidad"] = especialidad
                            print(f'El {medicos} se han modificado sus datos correctamente')
                            input("\n presione enter para continuar")
                            return
                        
        print("El medico no esta en la lista")
        input("\n presione enter para continuar")
        os.system('cls')
                        




    return


def menuMedicos(): # Menu Principal
    os.system('cls')
    medicos = [
        {"Medico_1":{"Nombre":"Gonzalez Juan",
                     "Edad":"30",
                     "DNI":(48120054,),
                     "Especialidad":"Traumatologo"}},

        {"Medico_2":{"Nombre":"Ortiz Mariana",
                     "Edad":"26",
                     "DNI":(45063213,),
                     "Especialidad":"Pediatra"}},

        {"Medico_3":{"Nombre":"Lopez Esteban",
                     "Edad":"37",
                     "DNI":(43170055,),
                     "Especialidad":"Oculista"}},             
    ]
    
    while True:
        print("\n" + "="*40)
        print("[0] , Salir del Programa") 
        print("[1] , Mostrar lista de medicos ") 
        print("[2] , Agregar medico " )
        print("[3] , Eliminar medico de la lista ")
        print("[4] , Modificar medico")
        print("="*40)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion == 1:
            mostrarLista(medicos)
        elif opcion == 2:
            agregarMedico(medicos)
        elif opcion == 3:
            eliminarMedico(medicos)
        elif opcion == 4:
            modificarMedico(medicos)
        elif opcion == 0:
            return
        else: 
            print("Opcion Invalida, Ingrese nuevamente los datos:")
            input("\nPresione Enter para continuar...")
       


def menuHospital(): # Submenu de medicos
    os.system('cls')
    while True:
        print("\n" + "="*40)
        print("[0] , Salir del programa " )
        print("[1] , Mostrar Menu de Medico " )
        print("[2] , Mostrar Menu de Paciente")
        print("[3] , Agendar Turno")
        print("[4] , Cancelar Turno")
        print("="*40)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion == 1:
            menuMedicos()
            os.system('cls')
        elif opcion == 2:
            eliminarMedicos()
        elif opcion == 3:
            agendarTurno()
        elif opcion == 4:
            eliminarTurno()
        elif opcion == 0:
            
            return

    

def main():
    menuHospital()
    os.system('cls')
    print("Saliendo del programa...")
main()