import modules.pe as pe
import modules.hashes as hashes
import modules.criptografia as cripto
import modules.scan as scan
import argparse

if __name__ == '__main__':

    ejemplos_pe = '''Ejemplo de uso:
            + Analizar el ejecutable portable sample.bin
                analyze -e sample.bin
                '''

    ejemplos_hash = '''Ejemplos de uso:
            + Obtener una lista de hashes de los archivos en todas las subcarpetas de C:\\Documentos\\trabajos\\
                hash -m dump -o hashesBase1.txt -r C:\\Documentos\\trabajos\\
            + Comparar los hashes de los archivos en todas las subcarpetas de C:\\Windows\\users\\files\\datos\\, con los almacenados en hashesBase1.txt
                hash --mode comp --hashfile hashesGuardados.txt --ruta C:\\Windows\\users\\files\\datos\\
                '''
    
    ejemplos_cripto = '''Ejemplos de uso:
            + Encriptar los datos encontrados en el archivo Ejem1.txt y guardar la llave de encripción con el nombre encript.key
                cripto -m encrp -a C:\\Users\\HP\\Desktop\\PIA\\Ejem1.txt -llv encript.key
            + Desencriptar los archivos que se encuentran en la carpeta DATOS con la llave encript.key
                cripto -m desen -a C:\\Users\\HP\\Desktop\\PIA\\DATOS -llv encript.key 
                '''

    ejemplos_scan = '''Ejemplos de uso:
            + Escanear con nmap el host 192.168.10.1
                scan -m nmap -i 192.168.10.1
            + Escanear con sockets el host 192.168.10.1
                scan --modo nmap --ip 192.168.10.1
                '''
                
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', help='Funciones')
    
    # Parser del modulo analyze
    parser_pe = subparsers.add_parser('analyze', help='Analiza un ejecutable portable, y genera su reporte con los resultados', epilog=ejemplos_pe, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_pe.add_argument('-e', '--exepath', dest='exepath', 
                        required=True, 
                        help='Ruta del ejecutable portable a analizar')
    parser_pe.add_argument('-o', '--outprefix', dest='outprefix', 
                        help='Prefijo para el nombre de archivo del reporte generado')

    # Parser del modulo hash
    parser_hash = subparsers.add_parser('hash',
                        help='Crea y compara hashes sha512 de todos los archivos en una carpeta', epilog=ejemplos_hash, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_hash.add_argument('-m', '--mode', dest='mode',
                        required=True,
                        help="Modo de ejecucion: dump (obtener), comp (comparar)")
    parser_hash.add_argument('-r', '--ruta', dest='path',
                        required=True, 
                        help="Especifica la carpeta para la obtencion de hashes (ruta absoluta)")
    parser_hash.add_argument('-o', '--outfile', dest='outfile',
                        help="Nombre del archivo a guardar con hashes; necesario para el modo dump")
    parser_hash.add_argument('-ha', '--hashfile', dest='hashfile',
                        help="Nombre del archivo con hashes contra el cual comparar; necesario para el modo comp")
    
    # Parser del modulo cripto
    parser_cripto = subparsers.add_parser('cripto', help='Realiza la extracción de datos sensibles en un archivo, así como su encriptación y desencriptación, y la generación de un reporte', epilog=ejemplos_cripto, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_cripto.add_argument('-m', '--modo', dest='modo',
                        required=True,
                        help="Modo de ejecución: encrp (encriptar) , desen (desencriptar)")                     
    parser_cripto.add_argument('-a', '--archivo', dest='archivo',
                        required=True, 
                        help="En Encriptación, especifica el archivo en donde se realizará la extracción(ruta absoluta). En Desencriptacion, especifica la carpeta en donde se encuentren los archivos encriptados (ruta absoluta)")
    parser_cripto.add_argument('-llv', '--llave', dest='llave',
                        required=True, 
                        help="Especifica el nombre de la llave")
    
    # Parser del modulo scan
    parser_scan = subparsers.add_parser('scan', help='Obtiene informacion de un host en la red, como puertos comunes abiertos, y sistema operativo detectado', epilog=ejemplos_scan, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_scan.add_argument('-m', '--modo', dest='modo',
                        required=True,
                        help="Modo de ejecucion: nmap (utiliza nmap), sock (utiliza socket)")
    parser_scan.add_argument('-i', '--ip', dest='host', metavar='DIRECCION_IP',
                        required=True,
                        help="Direccion del host a escanear")
                        

    args = parser.parse_args()
    if args.command:
        if args.command == 'analyze':
            if args.outprefix:
                ofile = pe.analyzePE(args.exepath, args.outprefix)
            else:
                ofile = pe.analyzePE(args.exepath)
            if ofile:
                print('Reporte del analisis guardado en:', ofile)
            else:
                print('Ocurrio un error inesperado')
        if args.command == 'hash':
            if args.mode == 'dump':
                if args.outfile:
                    try:
                        hashes.dumpHashes(args.path, args.outfile)
                    except Exception as e:
                        print("Ocurrió un error inesperado: " + str(e))
                else:
                    print('Se requiere un argumento para el parametro --outfile en el modo dump.')
            elif args.mode == 'comp':
                if args.hashfile:
                    try:
                        result = hashes.compareHashes(args.path, args.hashfile)
                        if result != None:
                            if result:
                                print('Coinciden los hashes')
                            else:
                                print('No coinciden los hashes')
                    except Exception as e:
                        print("Ocurrió un error inesperado: " + str(e))
                else:
                    print('Se requiere un argumento para el parametro --hashfile en el modo dump.')
            else:
                print('Modo no soportado. Validos: dump, comp')
        if args.command == 'cripto':
            if args.modo == 'encrp':
                cripto.recoleccion(args.archivo, args.llave)
            elif args.modo == 'desen':
                cripto.desencriptar(args.archivo, args.llave)
            else:
                print('Modo no soportado. Validos: encrp, desen')
        if args.command == 'scan':
            if args.modo == 'nmap':
                scan.results_nmap(args.host)
            elif args.modo == 'sock':
                scan.results_socket(args.host)
            else:
                print('Modo no soportado. Validos: nmap, sock')
    else:
        print('Debe proveer un modulo a usar (hash, analyze, cripto, scan)')
    
