import hashlib
import os
import argparse

#Validando la ruta de la carpeta
def ValidatePath(thePath):
    ''' Validate the Folder thePath
        it must exist and we must have rights
        to read from the folder.
        raise the appropriate error if either
        is not true
    '''
    # Valida que la ruta exista
    if not os.path.exists(thePath):
        raise argparse.ArgumentTypeError('La ruta no existe')

    # Valida que la ruta es leible
    if os.access(thePath, os.R_OK):
        return thePath
    else:
        raise argparse.ArgumentTypeError('La ruta no está disponible')

#Funciones que ejecuta el modo del script
def ListaHash():
    var1 = Hashes(tmpFile1, targetPath)
    SaveHash(var1)

def ComparationHashes():
    var2 = Hashes(tmpFile2, targetPath)
    SaveHash(var2)
    ComprobVerif(var2)

#Parseo de argumentos
info = 'Creador y comparador de hashes 512'
description="""Ejemplos de uso:
            +Obtener solo una lista de hashes
                -hash -f1 <hashesBase1.txt> -r <C:/Documentos/trabajos>
            +Comparar dos listas de Hashes (el primer archivo debe existir previamente)
                -comp -f1 <hashesBase2.txt> -r <C:/Windows/users/files/datos> -f2 <hashesBase1.txt> """
parser =argparse.ArgumentParser(description='Creación de hash y comparación de hashes',
                                    epilog = description,
                                    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-ha', '--hash',type=ListaHash,
        help="Modo de ejecución del script")
parser.add_argument('-co', '--comp', type=ComparationHashes,
        help="Modo para compara los hashes previos de un archivo con la lista de nuevos hashes generados")
parser.add_argument('-r', '--Ruta', type= ValidatePath,
        required=True, 
        help="Especifica la carpeta de obtencion de hashes. (ruta absoluta)")
parser.add_argument('-f1', '--file1', 
        required=True,
        help="Nombre del primer archivo con hashes")
parser.add_argument('-f2', '--file2',
        help="Nombre del segundo archivo con hashes (no es necesario tener un segundo arhivo, pues se crea antes de la comparación)")                 
args = parser.parse_args()   

tmpFile1    = args.file1
targetPath  = args.ruta
tmpFile2    = args.file2 

#Cambiando la ruta de la carpeta con archivos a hashear
#       tambien se crea un diccionario con los hashes y nombres de archivos
def Hashes(ruta):
    DictHashes = {}
    os.chdir(ruta)
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            try:
                print("Esta es la ruta\n",os.path.join(root, name))
                with open(name, 'rb') as file:
                    datos = file.read()
                    hash = hashlib.sha512(datos)
                    hasheado = hash.hexdigest()
                    DictHashes[name] = hasheado
                    file.close()
            except Exception as e:
                print("Ocurrió un error inesperado:" + str(e))
    return DictHashes
#=====================================================             

#Crear un archivo que guarda los datos actuales de hasheo
#               requiere un diccionario de la funcion hashes
def SaveHash(file, diccHash):
    try:
        with open(file, 'wb') as outFile:
            outFile.write(diccHash)
            outFile.close()           
    except Exception as err:
        print ("No se pudo crear un archvio de salida: "+ str(err))
        quit()

#Se comparan los hashes del documento anterior con los hashes del nuevo documento
def Verif_Hashes(d1, d2):
    if all( d1 == d2 ):
        return True
    else:
        return False
#Comprobación de datos   
def ComprobVerif(newDict):
    try:
            with open(tmpFile1, 'rb') as archivo1:
                DictHas=archivo1.read()
            archivo1.close()
            try:
                with open(tmpFile2, 'rb') as archivo2:
                    DictHas=archivo2.read()
                archivo2.close()
            except Exception as er:
                print("No se puede leer el archivo1: ",tmpFile2, "\n"+str(er))
                quit()

    except Exception as er:
        print("No se puede leer el archivo1: ",tmpFile1, "\n"+str(er))
        quit()
    
    if Verif_Hashes(DictHas, newDict):
        print("No se detectaron cambios")
    else:
        diff = Verif_Hashes(newDict, DictHas)
        print(diff)