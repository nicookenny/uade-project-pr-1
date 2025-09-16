import os

def mostrarLista(medicos): #Muestra el diccionario de las especialidades
    for especialista, medico in medicos.items():
        print("\n")
        print(especialista)
        for med,info in medico.items():
            print(med,info)
        
            
    return medicos

def agregarEspecialista(medico): #Agrega una especialidad al diccionario
    while True:
        especialidad = input("Ingresar especialidad: ")
        if especialidad not in medico:
            medico[especialidad] = {}
            medico[especialidad]["Medico_1"] = {"Nombre":None,"Estado":None}
            print("La especialidad se agrego correctamente")
            input("\nPresione Enter para continuar...")
            break
        
        else:
            print("La especialidad ya existe")
            input("\n presione enter para continuar")
            os.system('cls')
        
    return 
    
def menuMedicos(resultado): # Submenu de medicos
    os.system('cls')
    while True:
        print("\n" + "="*40)
        print("[1] , Agregar Medico " )
        print("[2] , Eliminar Medico de la lista ")
        print("[3] , Agendar Turno")
        print("[3] , Cancelar Turno")
        print("="*40)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion == 1:
            AgregarMedicos()
        elif opcion == 2:
            eliminarMedicos()
        elif opcion == 3:
            agendarTurno()
        elif opcion == 4:
            eliminarTurno()

    return


def menuHospital(): # Menu Principal
    os.system('cls')
    medicos = {
        "Traumatologo":{
            "Medico_1":{"Nombre":"Perez Juan", "Estado":"Disponible"},
            "Medico_2":{"Nombre":"Perez Juan", "Estado":"Disponible"},
            "Medico_3":{"Nombre":"Perez Juan", "Estado":"Disponible"},
            "Medico_4":{"Nombre":"Perez Juan", "Estado":"Disponible"},
        },
        "Pediatra":{
            "Medico_1":{"Nombre":"Perez Juan", "Estado":"Disponible"},
            "Medico_2":{"Nombre":"Perez Juan", "Estado":"Disponible"},
            "Medico_3":{"Nombre":"Perez Juan", "Estado":"Disponible"},
            "Medico_4":{"Nombre":"Perez Juan", "Estado":"Disponible"},
        },
        "Oculista":{
            "Medico_1":{"Nombre":"Perez Juan", "Estado":"Disponible"},
            "Medico_2":{"Nombre":"Perez Juan", "Estado":"Disponible"},
            "Medico_3":{"Nombre":"Perez Juan", "Estado":"Disponible"},
            "Medico_4":{"Nombre":"Perez Juan", "Estado":"Disponible"},
        }
               
    }

    while True:
        print("\n" + "="*40)
        print("[0] , Salir del Programa") 
        print("[1] , Mostrar lista de especialistas ") 
        print("[2] , Agregar Especialista " )
        print("[3] , Eliminar Especialista de la lista ")
        print("[4] , Ingresar menu de medicos")
        print("="*40)
        opcion = int(input("Ingresar una Opcion: "))
        if opcion == 1:
            resultado = mostrarLista(medicos)
        elif opcion == 2:
            agregarEspecialista(medicos)
        elif opcion == 4:
            menuMedicos(resultado)
        elif opcion == 0:
            os.system('cls')
            print("Saliendo del programa...")
            break
        else: 
            print("Opcion Invalida, Ingrese nuevamente los datos:")
            input("\nPresione Enter para continuar...")
        """ 
       elif opcion == 3:
            eliminarEspecialista()
            """
    return


def main():
    menuHospital()
main()