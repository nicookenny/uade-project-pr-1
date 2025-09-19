import os
import Datos
import Medicos
import Pacientes

def CargarDNI():
    dni = input("Ingresar número de documento: ")
    while not dni.isdigit() or len(dni) != 8:
        print("DNI inválido")
        dni = input("Ingresar otro número de documento: ")
    return int(dni)


def agendarTurno():
    lista = []
    diccionarioss = {}
    while True:
        Pacientes.mostrarLista()
        bandera = True
        dniPaciente = CargarDNI()
        for diccionarios in Datos.pacientes:
            for identificacion,dato in diccionarios.items(): 
                if dniPaciente == identificacion:
                    aux = identificacion
                    lista.append(diccionarios)
                    diccionarioss.update(diccionarios)
                    bandera = False
        
        if bandera == False:
            for diccionari in Datos.medicos:
                for medico, datos in diccionari.items():
                    for paciente in datos['Paciente']:
                                for dni,dato in paciente.items():
                                    if datos["Paciente"] != {} and dni == dniPaciente:
                                        print("El paciente ya tiene un turno agendado con otro médico.")
                                        input("\nPresione Enter para continuar...")
                                        return
            while True:
                Medicos.MostrartablaMedicos()
                band = False
                dniMedico = int(input("Ingresar numero de documento del medico con el que queres agendar un turno: "))
                for diccionario in Datos.medicos:
                    for medico,datos in diccionario.items():
                        if dniMedico == datos["DNI"]:
                            band = True
                            aux = datos
                            aux2 = diccionarios 
                            break
                
                if band == True:
                    if aux["Estado"] == 'Disponible':
                        aux['Estado'] = 'Ocupado'
                        aux['Paciente'] = lista
                        aux['Historial'].append(diccionarioss)
                        print("El turno se agendo correctamente")
                        input("\nPresione Enter para continuar...")
                        Medicos.MostrartablaMedicos()
                        return 
                    else:
                        print("El medico esta ocupado")
                        input("\nPresione Enter para continuar...")
                        os.system('cls')
                else:                 
                    print("El medico no esta en la lista")
                    input("\nPresione Enter para continuar...")
                    os.system('cls')
   

        print("El paciente no existe en la lista")
        input("\nPresione Enter para continuar...")
        os.system('cls')


                            


        
def cancelarTurno():
    while True:
        Pacientes.mostrarLista()
        bandera = True
        dniPaciente = CargarDNI()
        for diccionario in Datos.pacientes:
            for identificacion,dato in diccionario.items():
                if dniPaciente == identificacion:
                    aux = identificacion
                    bandera = False


        if bandera == False:            
            while True:
                bandera2 = False
                for diccionario in Datos.medicos:
                    for medico,datos in diccionario.items():
                        for paciente in datos['Paciente']:
                            for dni,dato in paciente.items():
                                if dniPaciente == dni:
                                    bandera2 = True

                if bandera2 == True:
                    break
                else:
                    print("El paciente no agendo nunca un turno, ingrese nuevamente los datos")
                    input("\nPresione Enter para continuar...")
                    while True:
                        os.system('cls')
                        Pacientes.mostrarLista()
                        bandera = True
                        dniPaciente = CargarDNI()
                        for diccionario in Datos.pacientes:
                            for identificacion,dato in diccionario.items():
                                if dniPaciente == identificacion:
                                    aux = identificacion
                                    bandera = False

                        if bandera == False:
                            break
                        else:
                            print("El paciente no existe en la lista")
                            input("\nPresione Enter para continuar...")

        if bandera == False:
            while True:
                Medicos.MostrartablaMedicos()
                band = False
                dniMedico = CargarDNI()
                for diccionario in Datos.medicos:
                    for medico,datos in diccionario.items():
                        for paciente in datos['Paciente']:
                            for dni,dato in paciente.items():
                                if dniMedico == datos["DNI"]:
                                    band = True
                                    aux2 = datos
                                    aux3 = dni
                   
                if band == True:
                    if aux2['Estado'] == 'Disponible':
                        band = False
                        print("ERROR, el medico esta disponible")
                        input("\nPresione Enter para continuar...")
                        os.system('cls')
                    else:
                        print(aux3)
                        input("\nPresione Enter para continuar...")
                        if dniPaciente == aux3:
                            aux2['Estado'] = 'Disponible'
                            aux2['Paciente'] = {}
                            print("El turno se cancelo correctamente")
                            input("\nPresione Enter para continuar...")
                            Medicos.MostrartablaMedicos()
                            return
                        else:
                            print(aux2['Paciente'])
                            print("El medico esta agendado con otro paciente, ingrese nuevamente todos los datos")
                            input("\nPresione Enter para continuar...")
                            return 
                    
                else:
                    print("El medico no esta en la lista")
                    input("\nPresione Enter para continuar...")
                    os.system('cls')

        print("El paciente no existe en la lista")
        input("\nPresione Enter para continuar...")
        os.system('cls')

def main():
    ...

main()