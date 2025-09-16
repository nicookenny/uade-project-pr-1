import os
from Diccionarios import medicos
from Diccionarios import pacientes



def agendarTurno():
    lista = []
    while True:
        bandera = True
        dniPaciente = int(input("Ingresar numero de documento del paciente: "))
        for diccionario in pacientes:
            for identificacion,dato in diccionario.items():
                if dniPaciente == identificacion:
                    aux = identificacion
                    lista.append(aux)
                    lista.append(dato)
                    bandera = False
                    break
        
        if bandera == False:
            for diccionari in medicos:
                for medico, datos in diccionari.items():
                    print(datos['Paciente'])
                    if datos["Paciente"] != "" and datos["Paciente"][0] == dniPaciente:
                        print("El paciente ya tiene un turno agendado con otro médico.")
                        input("\nPresione Enter para continuar...")
                        return
            while True:
                band = False
                dniMedico = int(input("Ingresar numero de documento del medico con el que queres agendar un turno: "))
                for diccionario in medicos:
                    for medico,datos in diccionario.items():
                        print(datos['DNI'][0])
                        if dniMedico == datos["DNI"][0]:
                            band = True
                            aux = datos 
                            break
                
                if band == True:
                    if aux["Estado"] == 'Disponible':
                        aux['Estado'] = 'Ocupado'
                        aux['Paciente'] = lista
                        print("El turno se agendo correctamente")
                        input("\nPresione Enter para continuar...")
                        return 
                    else:
                        print("El medico esta ocupado")
                        input("\nPresione Enter para continuar...")
                else:                 
                    print("El medico no esta en la lista")
                    input("\nPresione Enter para continuar...")
   

        print("El paciente no existe en la lista")
        input("\nPresione Enter para continuar...")


                            


        
def cancelarTurno():
    while True:
        bandera = True
        dniPaciente = int(input("Ingresar numero de documento del paciente: "))
        for diccionario in pacientes:
            for identificacion,dato in diccionario.items():
                if dniPaciente == identificacion:
                    aux = identificacion
                    bandera = False
                    break
        
        if bandera == False:
            while True:
                band = False
                dniMedico = int(input("Ingresar numero de documento del medico con el que queres cancelar el turno: "))
                for diccionario in medicos:
                    for medico,datos in diccionario.items():
                        if dniMedico == datos["DNI"][0] and aux == datos["Paciente"][0]:
                            band = True
                            aux = datos
                
                if band == True:
                    aux['Estado'] = 'Disponible'
                    aux['Paciente'] = 'Ninguno'
                    print("El turno se cancelo correctamente")
                    input("\nPresione Enter para continuar...")
                    return 
                else:
                    print(" ERROR el medico esta disponible")
                    input("\nPresione Enter para continuar...")
                            
                print("El medico no esta en la lista")
                input("\nPresione Enter para continuar...")
   

        print("El paciente no existe en la lista")
        input("\nPresione Enter para continuar...")



def main():
    ...

main()