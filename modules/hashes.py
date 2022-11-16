#Autor: Yosafat Aguirre Hernandez
import hashlib
import os
import pickle

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
        raise FileNotFoundError('La ruta no está disponible')

    # Valida que la ruta es leible
    if os.access(thePath, os.R_OK):
        return thePath
    else:
        raise FileNotFoundError('La ruta no está disponible')

# Cambiando la ruta de la carpeta con archivos a hashear
# se crea un conjunto con los hashes y nombres de archivos
def Hashes(ruta):
    setHashes = set()
    os.chdir(ruta)
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
                with open(os.path.join(root, name), 'rb') as file:
                    datos = file.read()
                    hash = hashlib.sha512(datos)
                    hasheado = hash.hexdigest()
                    setHashes.add(hasheado)
    return setHashes
#=====================================================

# Dumpea un archivo en formato pickle el set con hashes
def dumpHashes(path, outfile):
    hashes = Hashes(path)
    with open(outfile, 'wb') as out:
        pickle.dump(hashes, out)
        print('Archivo de hashes guardado en:', outfile)


def compareHashes(path, path_comp):
    # Obtiene un set con hashes, carga el ubicado en path_comp (pickled), y los compara
    hashes = Hashes(path)
    with open(path_comp, 'rb') as archivo1:
        setHashes = pickle.load(archivo1)
        if type(setHashes) == set:
            return setHashes == hashes
    return None

