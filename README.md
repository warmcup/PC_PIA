# PC_PIA

## Propósito
Este proyecto busca proveer una herramienta que lleve a cabo tareas relacionadas con el rubro de la ciberseguridad, aplicando los conocimientos adquiridos a lo largo del curso de 'Programación para Ciberseguridad'.

## Instalación
```powershell
git clone https://github.com/warmcup/PC_PIA
cd PC_PIA
pip3 install -r requirements.txt
```
Además de los pasos anteriores, se debe de [instalar bash](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/) en su sistema, y [nmap](https://phoenixnap.com/kb/how-to-install-use-nmap-scanning-linux) para dicho subsistema.

> **Advertencia:** este software solo asegura compatibilidad con Windows 10 y Windows 11, usando Python 3.10+

## Funcionalidad
El programa posee 4 módulos que realizan distintas tareas. Para acceder a ellas, se deben utilizar diferentes argumentos al llamar al script.

### Módulo hash
Genera y compara sumas de comprobación para toda una carpeta. Estas son procesadas como archivos que el programa produce.

#### Argumentos admitidos

| Argumento     | Descripción |
|:-------------:|:---------------:|
| -m MODE, --mode MODE |  Modo de ejecucion: dump (obtener), comp (comparar) |
| -r PATH, --ruta PATH | Especifica la carpeta para la obtencion de hashes (ruta absoluta) |
| -o OUTFILE, --outfile OUTFILE | Nombre del archivo a guardar con hashes; necesario para el modo dump |
| -ha HASHFILE, --hashfile HASHFILE | Nombre del archivo con hashes contra el cual comparar; necesario para el modo comp |
              
#### Ejemplos de uso
Obtener una lista de hashes de los archivos en todas las subcarpetas de C:\Documentos\trabajos\:
```powershell
python main.py hash -m dump -o hashesBase1.txt -r C:\Documentos\trabajos\
```

Comparar los hashes de los archivos en todas las subcarpetas de C:\Windows\users\files\datos\, con los almacenados en hashesBase1.txt:
```powershell
python main.py hash --mode comp --hashfile hashesGuardados.txt --ruta C:\Windows\users\files\datos\
```

### Módulo analyze
Analiza un ejecutable portable (PE). Crea un reporte con la información encontrada sobre él, entre la que se encuentra:
+ Fecha de compilación
+ Detecciones en VirusTotal (búsqueda por checksum)*
+ Funciones del sistema llamadas
+ Representación gráfica del código en lenguaje ensamblador

***Para hacer uso de la funcionalidad de busqueda por checksum en VirusTotal, se debe editar el archivo modules/pe.py:**

```python
def queryVT(checksum):
    ...
    auth = {'x-apikey' : 'SU_API_KEY'}
    ...
```

#### Argumentos admitidos

| Argumento     | Descripción |
|:-------------:|:---------------:|
| -e EXEPATH, --exepath EXEPATH |  Ruta del ejecutable portable a analizar |
| -o OUTPREFIX, --outprefix OUTPREFIX | Prefijo para el nombre de archivo del reporte generado |
              
#### Ejemplo de uso
Analizar el ejecutable portable sample.bin:
```powershell
python main.py analyze -e sample.bin
```

### Módulo cripto
Realiza la extracción de datos específicos (correos, ip, usuarios) en archivos, para la encriptación y desencriptación de los datos, para generar un reporte. 

| Argumento     | Descripción |
|:-------------:|:---------------:|
| -m MODO, --modo MODO |  Modo de ejecución: encrp (encriptar) , desen (desencriptar) |
| -a ARCHIVO, --archivo ARCHIVO | En Encriptación, especifica el archivo en donde se realizará la extracción(ruta absoluta). En Desencriptacion, especifica la carpeta en donde se encuentren los archivos encriptados(ruta absoluta)." |
| -llv LLAVE, --llave LLAVE | Especifica el nombre de la llave (recuerda el .key) |
              
#### Ejemplos de uso
Encriptar los datos encontrados en el archivo Ejem1.txt y guardar la llave de encripción con el nombre encript.key
```powershell
python main.py cripto -m encrp -a C:\Users\HP\Desktop\PIA\Ejem1.txt -llv encript.key
```

Desencriptar los archivos que se encuentran en la carpeta DATOS con la llave encript.key
```powershell
python main.py cripto -m desen -a C:\Users\HP\Desktop\PIA\DATOS -llv encript.key
```



### Módulo scan

## Créditos
+ **@al3xand3r07**: módulo hash
+ **@Angeltrst03**: módulo scan
+ **@BsIsraU08**: módulo cripto
+ **@warmcup**: módulo analyze
+ **Daniel Gibert (daniel.gibertlla@gmail.com)**: desarrollador del módulo pe-parser
