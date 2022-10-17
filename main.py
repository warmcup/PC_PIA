import modules.pe as pe
import argparse

if __name__ == '__main__':

    # Pendiente, agregar ayuda aquí
    desc = '''
    
    '''
    parser = argparse.ArgumentParser(epilog=desc)
    subparsers = parser.add_subparsers(dest='command', help='Funciones')
    parser_pe = subparsers.add_parser('analyze', help='Analiza un ejecutable portable, y genera su reporte con los resultados')
    parser_pe.add_argument('--exepath', required=True, help='Ruta del ejecutable portable a analizar')
    parser_pe.add_argument('--outprefix', required=False, help='Prefijo para el nombre de archivo del reporte generado')

    args = parser.parse_args()

    if args.command:
        if args.command == 'analyze':
            if args.outprefix:
                pe.analyzePEExe(args.exepath, args.outprefix)
            else:
                pe.analyzePEExe(args.exepath)

    