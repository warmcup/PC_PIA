# Autor: Juan Angel Garza Castillo

import base64
import requests
import hashlib
import time
import logging
import io
import sys
from unicodedata import decimal
from pe_parser.asm_parser import AssemblyParser
import pefile
import matplotlib.pyplot as plot

# Request para obtención de detecciones en formato "malicioso/total de analisis"
# de la base de datos de VirusTotal
def queryVT(checksum):
    query = {'query' : checksum}
    auth = {'x-apikey' : 'e174abb47cb330a297190406eb71bdda71a1fee63b1ba756373342c43c48946b'} # Cambiado por privacidad
    results = requests.get("https://www.virustotal.com/api/v3/search", params=query, headers=auth)
    ret = None
    if results.status_code == 200 and results.json()['data']:
        malicious =  results.json()['data'][0]['attributes']['last_analysis_stats']['malicious']
        total =  results.json()['data'][0]['attributes']['last_analysis_stats']['undetected'] + malicious
        ret = str(malicious) + "/" + str(total)
    return ret

# Análisis del ejecutable con base en su codigo en lenguaje ensamblador, y sus detecciones en virustotal
def analyzePEExe(path):
    ts = str(int(time.time()))
    logging.basicConfig(level=logging.INFO, filename="analyzePEExeLOG-" + ts + ".log")
    logging.info("Iniciado analisis de ejecutable")
    try:
        # Extracción de metadatos del encabezado PE
        pe = pefile.PE(path)
        properties = {'arch' : '', 'compilationDate' : ''}
        if hex(pe.FILE_HEADER.Machine) == '0x14c':
            properties['arch'] = "x86"
        else:
            properties['arch'] = "x64"
        properties['compilationDate'] = int(pe.FILE_HEADER.dump_dict()['TimeDateStamp']['Value'].split('[')[0][:-1], 16)
        logging.info("Obtenidos metadatos")

        # Obtención de suma de comprobación
        checksum = ""
        with open(path, "rb") as file:
            checksum = hashlib.sha256(file.read()).hexdigest()
        logging.info("Calculada suma de comprobacion")

        # Lookup en VirusTotal, por checksum
        logging.info("Haciendo request a VT")
        detections = queryVT(checksum)
        if not detections:
            logging.error("Request fallo")
            detections = "No disponible"

        # Uso de pe_parser para obtención de información del ejecutable, con base en su código en ASM
        asm_parser = AssemblyParser(path)
        raw_img = io.BytesIO()
        asm_img = asm_parser.convert_asm_to_img()
        plot.axis("off")
        plot.imshow(asm_img, cmap="gray", interpolation="nearest")
        plot.savefig(raw_img, format='jpg')
        raw_img.seek(0)
        base64_asm_img = base64.b64encode(raw_img.read())
        api_features = asm_parser.extract_API_features()
        api_calls_list = []
        for a in api_features:
            n = api_features.get(a)
            if n:
                api_calls_list.append("<td>" + a[8:] + "()" + "</td><td>" + str(n) + "</td></tr>")
        api_calls_str = "<tr>" + "<tr>".join(api_calls_list)

        #Construcción del reporte
        html_report = """
        <html>
            <head>
                <title>Reporte de analisis de ejecutable</title>
            </head>
            <body>
                <h2>Reporte de analisis de ejecutable</h2>
                <p>
                Ruta del ejecutable: {} <br>
                Suma de comprobacion (SHA256): {} <br>
                Arquitectura del ejecutable: {} <br>
                Timestamp de compilacion del ejecutable: {} <br>
                Detecciones en VirusTotal: {} <br>
                </p>
                <h3>Frecuencia de llamada a APIs comunes del sistema:</h3>
                <table>
                <tr>
                    <th>Funcion</th>
                    <th>Frecuencia</th>
                </tr>
                    {}
                </table>
                <h3>Representacion grafica de su codigo en lenguaje ensamblador:</h3>
                <img src="data:image/png;base64, {}"/>
                    </body>
        </html>
        """.format(path, checksum, properties['arch'], properties['compilationDate'], detections, api_calls_str, base64_asm_img.decode())
        report_filename = "analyzePEExeReport-" + ts + ".html"
        logging.info("Finalizado analisis de ejecutable, reporte guardado en " + report_filename)
        with open(report_filename, "w") as report_out:
            report_out.write(html_report)
        return report_filename
    except Exception as e:
        logging.error("Excepcion en analyzePEExe(): {}. Saliendo de la rutina...".format(e))
        return None

