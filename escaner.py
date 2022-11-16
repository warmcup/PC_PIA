import socket
import subprocess


print(subprocessrun.(nmap2.sh))



#funcion scan 
def scan(ip,port):
    #se abre la conexion socket
    socket_obj=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result= socket_obj.connect_ex((ip,port))
    socket_obj.close()
    return result

#se definen puertos
ports = [21,22,25,80,443]
 for i in range (1,256):
     addr=("ingrese la ip a escanear")
     ip= "addr.{}".format(i)
     for port in ports
     res = scan(ip,port)
     if res ==o:
         print (ip,port,"open")
         else:
             print (ip,port,"close ")

     
