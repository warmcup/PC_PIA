import socket
import subprocess

#funcion scan 
def scan(ip,port):
    #se abre la conexion socket
    socket_obj=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result= socket_obj.connect_ex((ip,port))
    socket_obj.close()
    return result

def results_socket(ip):
    ports = [21,22,25,80,443]
    results = []
    try:
        for port in ports:
            res = scan(ip,port)
            if res == 0:
                results.append((str(port), 'abierto'))
            else:
                results.append((str(port), 'cerrado'))
        for res in results:
            print(ip + ':' + res[0], 'esta', res[1])

    except Exception as e:
        print('Ocurrio un error inesperado:', str(e))

def results_nmap(ip):
    try:
        result = (subprocess.check_output('bash modules/nmap.sh {}'.format(ip), shell = True)).decode()
        if result:
            print('Detectado sistema operativo:', result.capitalize())
        else:
            print('No se pudo detectar un sistema operativo en el host')
        print('Resultados del scan con nmap guardado en: scan.txt')
    except Exception as e:
        print('Ocurrio un error inesperado:', str(e))