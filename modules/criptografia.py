#Autor: Jesús Israel Bolaños Uvalle
#Matrícula: 2005587

import re
import os
from openpyxl import Workbook
from cryptography.fernet import Fernet


                                    #################### EXPRESIONES REGULARES #######################

expcorreos=r'[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])'

expIp= r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

expusuarios=  r'(user=[a-zA-Z0-9!#$%&*+/=?^_`.@{|}~-]+)'


                  ############################################### BLOQUE DE FUNCIONES #######################################################

#Función para la extracción de los datos
def recoleccion(archivo, llave):
    try:
        #Lee el contenido del archivo
        with open(archivo,'r') as file:
            contenido= file.read()
            
        #Buscamos los correos, ip y usuarios en el archivo
        buscar1=re.findall(expcorreos, contenido)
        buscar2=re.findall(expIp, contenido)
        buscar3=re.findall(expusuarios, contenido)
        
        #Creamos la carpeta DATOs
        try:
            os.mkdir('DATOS_PIA')
            a = os.path.abspath('DATOS_PIA')
            os.chdir(a)
        except FileExistsError:
            a = os.path.abspath('DATOS_PIA')
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
            nom1= 'Correos.rz'
            with open('Correos.rz','a') as file:
                file.write(x)
                file.write('\n')
        encriptar(nom1, llave)

        for x in buscar2:
            nom2='Ips.rz'
            with open('Ips.rz', 'a') as file:
                file.write(x)
                file.write('\n')
        encriptar(nom2, llave)

        for x in buscar3:
            nom3='Usuarios.rz'
            with open('Usuarios.rz', 'a') as file:
                file.write(x)
                file.write('\n')
        encriptar(nom3, llave)
    except:
        print('Ocurrio un error en la recolección')
                        ####################################### BLOQUE DE ENCRIPTACION #######################################
    
def encriptar(nom_archivo, llave):
  try:
    with open(nom_archivo,"rb") as file:
        archivo_info = file.read()
    encrypted_data = llave.encrypt(archivo_info)
    with open(nom_archivo, 'wb') as file:
        file.write(encrypted_data)
  except:
    print('Ocurrio un error en la encriptación')


                            ####################################### BLOQUE DE DESENCRIPTACION ###############################################
               
def desencriptar(nom_carpeta, llave):
    try:
        os.chdir(nom_carpeta)
        #Llamamos a la llave para utilizarla
        def call_key():
            return open(llave, "rb").read()
        
        key= call_key()
        llave = Fernet(key)

        lista=[]
        #Buscamos en el directorio todos los archivos que tengan la terminación .rz
        for archivo in os.listdir():
            if archivo.endswith(".rz"):
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
            buscar1=re.findall(expcorreos, contenido)
            buscar2=re.findall(expIp, contenido)
            buscar3=re.findall(expusuarios, contenido)

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
        
    except:
        print('Hubo un error en la desencriptación')
