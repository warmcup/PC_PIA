#Autor: Jesús Israel Bolaños Uvalle


import re
import os
import errno
import sys
from openpyxl import Workbook
from cryptography.fernet import Fernet


                                    #################### EXPRESIONES REGULARES #######################

expcorreos=r'[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])'

expIp= r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

expusuarios=  r'user=([a-z0-9!#$%&*+/=?^_`.@{|}~-]+)'

expnumeros= r'[\(]?[\+]?(\d{2}|\d{3})[\)]?[\s]?((\d{6}|\d{8})|(\d{3}[\*\.\-]){2}\d{3}|(\d{2}[\*\.\-\s]){3}\d{2}|(\d{4}[\*\.\-\s]){1}\d{4})|\d{8}|\d{10}|\d{12}'



                  ############################################### BLOQUE DE FUNCIONES #######################################################

#Funcion para buscar el archivo en toda la PC
def buscaruta(ruta):
    target = ruta
    initial_dir = 'C:\\'

    path = ''
    for root, _, files in os.walk(initial_dir):
        if target in files:
           global archivo
           archivo = os.path.join(root, target)
           break

#Funcion para retroceder un directorio antes de la carpeta, salirme de ella        
def separador():
    separador = os.path.sep
    dir_actual = os.path.dirname(os.path.abspath('DATOS'))
    global directorio
    directorio = separador.join(dir_actual.split(separador)[:-1])


#Función para la extracción de los datos
def recoleccion():
    while True:
        nombre= input("Nombre del archivo en donde se realizará la extracción: ")
    
        #Llamamos la funcion "buscaruta" para buscar el archivo en toda la PC
        print("Buscando archivo...\n")
        buscaruta(nombre)


            
        #Lee el contenido del archivo
        with open(archivo,'r') as file:
            contenido= file.read()
            
        #Buscamos los correos en el contenido
        buscar=re.findall(expregular, contenido)
        #print(buscar)
        
        #Verificamos que haya encontrado coincidencias con la regex
        w= len(buscar)
        if len(buscar) > 0:
            
        #Creo una carpeta para ahi meter la key y el archivo con la información encriptada
        #Compruebo si exite la carpeta ya creada
            
            try:
                os.mkdir('DATOS')
                a = os.path.abspath('DATOS')
                os.chdir(a)
            except FileExistsError:
                a = os.path.abspath('DATOS')
                os.chdir(a)
            

            for x in buscar:
                with open(nomdatos, 'a') as file:
                    file.write(x)
                    file.write('\n')
            encriptar(nomdatos)
            separador()
            os.chdir(directorio)
            break
        print("\n##### No se encontraron coincidencias del dato solicitado #####\n")
        print("##### Ingrese otro archivo #####\n")
        continue



        
                        ####################################### BLOQUE DE ENCRIPTACION #######################################
    
def encriptar(nom_archivo):
    #La creación de la llave
    llave1= input("Ingrese el nombre con el que quiera guardar su llave: ")
    def genwrite():
            key = Fernet.generate_key()
            with open(llave1 + '.key', "wb") as key_file:
                    key_file.write(key)

    genwrite()
    
    # Leemos el archivo que tiene la llave
    def call_key():
            return open(llave1 + '.key', "rb").read()
    key= call_key()
    a= Fernet(key)
    with open(nom_archivo,"rb") as file:
        archivo_info = file.read()
    encrypted_data = a.encrypt(archivo_info)
    with open(nom_archivo, 'wb') as file:
        file.write(encrypted_data)


                            ####################################### BLOQUE DE DESENCRIPTACION ###############################################
               
        
def desencriptar(nom_archivo):
    #Nos movemos a la carpeta en donde se encuentran los datos encriptados
    a= os.path.abspath('DATOS')
    #os.chdir(a)
    #print(a)
    def call_key():
        llave=input("Ingrese el nombre del archivo que contiene su llave: ")
        return open(llave, "rb").read()
    
    try:
        key= call_key()
        
        a= Fernet(key)
        try:
            #Desencriptamos los datos
            with open(nom_archivo,"rb") as file:
                encrypted_data = file.read()
            decrypted_data = a.decrypt(encrypted_data)
            with open(nom_archivo, 'wb') as file:
                file.write(decrypted_data)
                
            #Activamos el excel para meter la información encriptada
            with open(nom_archivo,'r') as file:
                contenido= file.read()
            buscar=re.findall(expregular, contenido)

            hoja['B1'] = "CORREOS"
            hoja['G1'] = "IPs"
            hoja['J1'] = 'Usuarios'
            hoja['M1'] = 'Números'
            if expregular == expcorreos:
                long= len(buscar)
                for x in range(long):
                    hoja[f'A{x +2}'] = buscar[x]
                
            elif expregular == expIp:
                long= len(buscar)
                for x in range(long):
                    hoja[f'F{x +2}'] = buscar[x]
                    
            elif expregular == expusuarios:
                long= len(buscar)
                for x in range(long):
                    hoja[f'I{x +2}'] = buscar[x]

            elif expregular == expusurips:
                long= len(buscar)
                for x in range(long):
                    hoja[f'L{x +2}'] = buscar[x]
                    
            separador()
            os.chdir(directorio)
        except:
            print('\nEl archivo encriptado no se encuentra en la carpeta!')
            separador()
            os.chdir(directorio)
    except FileNotFoundError:
        print('\nLa llave no se encuentra en la carpeta!\n')
        print('Verificar el nombre correcto del archivo que contiene la llave!\n')
        separador()
        os.chdir(directorio)
        exit
        
                        ####################################### MENU ###############################################
        
print("Bienvenido a la tarea de encriptación de datos\n")
y='1'
reporte=Workbook()
hoja= reporte.active
while y == '1':

    print("[1] ENCRIPTAR CORREOS")
    print("[2] ENCRIPTAR IP")
    print("[3] ENCRIPTAR Usuarios")
    print("[4] ENCRIPTAR Numeros")
    print("[5] DESENCRIPTAR CORREOS Y HACER UN REPORTE")
    print("[6] DESENCRIPTAR IP Y HACER UN REPORTE")
    print("[7] DESENCRIPTAR Usuarios Y HACER UN REPORTE")
    print("[8] DESENCRIPTAR Numeros Y HACER UN REPORTE")
    #a= os.getcwd()
    #print(a)
    opciones= input("¿Qué desea hacer? ")

    if opciones == '1':
        expregular= expcorreos
        nomdatos='Correos'
        recoleccion()
        print("\nEncriptación correcta!! :D\n")
        
    elif opciones == '2':
        expregular= expIp
        nomdatos='IPs'
        recoleccion()
        print("\nEncriptación correcta!! :D\n")
        
    elif opciones == '3':
        expregular= expusuarios
        nomdatos='Usuarios'
        recoleccion()
        print("\nEncriptación correcta!! :D\n")
        
    elif opciones == '4':
        expregular= expnumeros
        nomdatos='Numeros'
        recoleccion()
        print("\nEncriptación correcta!! :D\n")
        
    elif opciones == '5':
        expregular= expcorreos
        nom_archivo= input("Nombre del archivo encriptado: ")
        desencriptar(nom_archivo)
        print("\nDesencriptación correcta!! :D\n")

    elif opciones == '6':
        nom_archivo= input("Nombre del archivo encriptado: ")
        expregular= expIp
        desencriptar(nom_archivo)
        print("\nDesencriptación correcta!! :D\n")
        
    elif opciones == '7':
        expregular= expusuarios
        nom_archivo= input("Nombre del archivo encriptado: ")
        desencriptar(nom_archivo)
        print("\nDesencriptación correcta!! :D\n")
        
    elif opciones == '8':
        expregular= expnumeros
        nom_archivo= input("Nombre del archivo encriptado: ")
        desencriptar(nom_archivo)
        print("\nDesencriptación correcta!! :D\n")
        
    y= input("¿Desea hacer otra cosa? [1]SI, [2]NO: ")
    #a= os.getcwd()
    #print(a)
reporte.save("Reporte de Encriptación.xlsx")
