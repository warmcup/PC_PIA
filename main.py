import modules.pe as pe
import modules.hashes as hashes
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
                 cripto -m encrp -a C:\Users\HP\Desktop\PIA\Ejem1.txt -llv encript.key
            + Desencriptar los archivos que se encuentran en la carpeta DATOS con la llave encript.key
                 cripto -m desen -a C:\Users\HP\Desktop\PIA\DATOS -llv encript.key     
                 '''

    parser = argparse.ArgumentParser(epilog=desc)
    subparsers = parser.add_subparsers(dest='command', help='Funciones')
    parser_pe = subparsers.add_parser('analyze', help='Analiza un ejecutable portable, y genera su reporte con los resultados', epilog=ejemplos_pe, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_pe.add_argument('-e', '--exepath', required=True, help='Ruta del ejecutable portable a analizar')
    parser_pe.add_argument('-o', '--outprefix', help='Prefijo para el nombre de archivo del reporte generado')
    parser_hash = subparsers.add_parser('hash', help='Crea y compara hashes sha512 de todos los archivos en una carpeta', epilog=ejemplos_hash, formatter_class=argparse.RawDescriptionHelpFormatter)
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
        
    args = parser.parse_args()

    if args.command:
        if args.command == 'analyze':
            if args.outprefix:
                pe.analyzePE(args.exepath, args.outprefix)
            else:
                pe.analyzePE(args.exepath)
        if args.command == 'hash':
            if args.mode == 'dump':
                if args.outfile:
                    hashes.dumpHashes(args.path, args.outfile)
                else:
                    print('Se requiere un argumento para el parametro --outfile en el modo dump.')
            if args.mode == 'comp':
                if args.hashfile:
                    result = hashes.compareHashes(args.path, args.hashfile)
                    if result != None:
                        if result:
                            print('Coinciden los hashes')
                        else:
                            print('No coinciden')
                else:
                    print('Se requiere un argumento para el parametro --hashfile en el modo dump.')

    
