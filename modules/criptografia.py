#Autor: Jesús Israel Bolaños Uvalle

import argparse
import re
import os
import errno
import sys
from openpyxl import Workbook
from cryptography.fernet import Fernet


                                    #################### EXPRESIONES REGULARES #######################

expcorreos=r'[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])'

expIp= r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

expusuarios=  r'(user=[a-zA-Z0-9!#$%&*+/=?^_`.@{|}~-]+)'


                  ############################################### BLOQUE DE FUNCIONES #######################################################

#Función para la extracción de los datos
def recoleccion(archivo, llave):
    while True:
      
        #Lee el contenido del archivo
        with open(archivo,'r') as file:
            contenido= file.read()
            
        #Buscamos los correos, ip y usuarios en el archivo
        buscar1=re.findall(expregular1, contenido)
        buscar2=re.findall(expregular2, contenido)
        buscar3=re.findall(expregular3, contenido)
        
        #Creamos la carpeta DATOs
        try:
            os.mkdir('DATOS')
            a = os.path.abspath('DATOS')
            os.chdir(a)
        except FileExistsError:
            a = os.path.abspath('DATOS')
            os.chdir(a)
                
    #La creación de la llave
        def genwrite():
            key = Fernet.generate_key()
            with open(llave, "wb") as key_file:
                key_file.write(key)

        genwrite()
    
    # Leemos el archivo que tiene la llave
        def call_key():
            return open(llave, "rb").read()

        key= call_key()
        llave = Fernet(key)

    # Buscamos los correos, ip y usuarios, dependiendo cual encuentre lo va agarrar en una archivo en especifico
        for x in buscar1:
            nom1= 'Correos.txt'
            with open('Correos.txt', 'a') as file:
                file.write(x)
                file.write('\n')
        encriptar(nom1, llave)

        for x in buscar2:
            nom2='Ips.txt'
            with open('Ips.txt', 'a') as file:
                file.write(x)
                file.write('\n')
        encriptar(nom2, llave)

        for x in buscar3:
            nom3='Usuarios.txt'
            with open('Usuarios.txt', 'a') as file:
                file.write(x)
                file.write('\n')
        encriptar(nom3, llave)

        break



        
                        ####################################### BLOQUE DE ENCRIPTACION #######################################
    
def encriptar(nom_archivo, llave):
    
    with open(nom_archivo,"rb") as file:
        archivo_info = file.read()
    encrypted_data = llave.encrypt(archivo_info)
    with open(nom_archivo, 'wb') as file:
        file.write(encrypted_data)


                            ####################################### BLOQUE DE DESENCRIPTACION ###############################################
               
def desencriptar(nom_carpeta, llave):

    os.chdir(nom_carpeta)

    #Llamamos a la llave para utilizarla
    def call_key():
        return open(llave, "rb").read()
    
    key= call_key()
    llave = Fernet(key)
    
    try:
        lista=[]

        #Buscamos en el directorio todos los archivos que tengan la terminación .txt
        for archivo in os.listdir():
            if archivo.endswith(".txt"):
                lista.append(archivo)

        #Cada archivo que se encontro se le va a desencriptar
        for archivo in lista:
            #Desencriptamos los datos
            with open(archivo,"rb") as file:
                encrypted_data = file.read()
            decrypted_data = llave.decrypt(encrypted_data)
            with open(archivo, 'wb') as file:
                file.write(decrypted_data)
                
        #Activamos el excel para meter la información desencriptada
        reporte=Workbook()
        hoja= reporte.active

        hoja['B1'] = "CORREOS"
        hoja['G1'] = "IPs"
        hoja['J1'] = 'Usuarios'

        #En cada archivo vamos a buscar si tiene correos, ip o usuarios
        for archivo in lista:
            with open(archivo,'r') as file:
                contenido= file.read()
            buscar1=re.findall(expregular1, contenido)
            buscar2=re.findall(expregular2, contenido)
            buscar3=re.findall(expregular3, contenido)

            co= len(buscar1)
            ip= len(buscar2)
            us= len(buscar3)

        #Se agrega al excel lo que se encontró en el archivo   
            for correo in range(co):
                hoja[f'A{correo +2}'] = buscar1[correo]

            for ip in range(ip):
                hoja[f'F{ip +2}'] = buscar2[ip]

            for usuario in range(us):
                hoja[f'I{usuario +2}'] = buscar3[usuario]

        reporte.save("Reporte de Encriptación.xlsx")
        
    except FileNotFoundError:
        print('\nHay un archivo que no se puede desencriptar')

                        ####################################### MENU ###############################################


parser_crip = argparse.ArgumentParser()
parser_crip.add_argument('-m', '--modo', dest='modo',
                        required=True,
                        help="Modo de encriptar: encrp .  Modo desencriptar: desen .")
                        
parser_crip.add_argument('-a', '--archivo', dest='archivo',
                        required=True, 
                        help="En el modo de Encriptación, especifica el archivo en donde se realizará la extracción(ruta absoluta). En el modo de Desencriptacion, espcifica la carpeta en donde se encuentren los archivos encriptados(ruta absoluta).")

parser_crip.add_argument('-llv', '--llave', dest='llave',
                        required=True, 
                        help="Especifica el nombre de la llave")
    
args = parser_crip.parse_args()
modo = args.modo
archivo = args.archivo
llave = args.llave

if modo == 'encrp':
    expregular1= expcorreos
    expregular2= expIp
    expregular3= expusuarios

    recoleccion(archivo, llave)
    print("\nEncriptación correcta!! :D\n")
        
elif modo == 'desen':
    expregular1= expcorreos
    expregular2= expIp
    expregular3= expusuarios
    
    desencriptar(archivo, llave)
    print("\nDesencriptación correcta!! :D\n")
    
