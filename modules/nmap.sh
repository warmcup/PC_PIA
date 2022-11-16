#asignamos a la variable ip el primer valor que ingresamos a la linea de comandos
ip=$1
#ejecutamos un ping y lo guardamos en un archivo llamado ping.log
ping -c 1 $ip > ping.log
#se busca en el archivo el ttl para verificar que SO usa el host
for i in $(seq 60 70); do
    if [ $(grep ttl=$i ping.log -c) -eq 1 ]; then
        echo 'linux'
        break
    fi
done

for i in $(seq 100 200); do
    if [ $(grep ttl=$i ping.log -c) -eq 1 ]; then
    echo 'windows'
    break
    fi
done

#se borra el archivo anteriormente generado
rm ping.log

#hacemos un scaneo rapido usando nmap
nmap -p21,22,25,80,443 $ip > scan.txt
