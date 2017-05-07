# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: sv_information.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco & Yonathan Mtz.
# Version: 1.2 Abril 2017
# Descripción:
#
#   Este archivo define el rol de un servicio. Su función general es porporcionar en un objeto JSON
#   información detallada acerca de una pelicula o una serie en particular haciendo uso del API proporcionada
#   por IMDb ('https://www.imdb.com/').
#   
#   
#
#                                        sv_information.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Ofrecer un JSON que  | - Utiliza el API de    |
#           |    Procesador de      |    contenga información |   IMDb.                |
#           |     comentarios       |    detallada de pelí-   | - Devuelve un JSON con |
#           |       de IMDb         |    culas o series en    |   datos de la serie o  |
#           |                       |    particular.          |   pelicula en cuestión.|
#           +-----------------------+-------------------------+------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8084/api/v1/information?t=matrix
#
from flask import Flask, abort, render_template, request
import os, urllib, json, oauth2, settings_analisisSentimiento, requests
from twython import Twython

app = Flask (__name__)

@app.route("/api/v1/sentiment", methods=['POST'])
def get_information():
        comments = request.get_json()
        
        total = len(comments["comments"])
        
        if total > 0:
 
                pos = 0
                neg = 0
                neu = 0
                                       
                for c in comments["comments"]:
                        endpoint = 'https://japerk-text-processing.p.mashape.com/sentiment/'
                        headers = {
                                 'X-Mashape-Key': settings_analisisSentimiento.MASHAPE_KEY,
                                 }
                        payload = {
                                'language': 'english',
                                'text': c,
                        }
                        response = requests.post(endpoint, headers=headers, data=payload)
                        response = response.json()

                        if response['label'] == "pos":
                                pos += 1
                        elif response['label'] == "neg":
                                neg += 1
                        else:
                                neu += 1

                statistic = {
                        'pos': pos,
                        'neg': neg,
                        'neu': neu,
                        'tot': total,
                                }
                
                statistic = json.dumps(statistic, ensure_ascii=False)
                return statistic

	else:
		# Se devuelve un error 400 para indicar que el servicio no puede funcionar sin parámetro
		abort(400)


if __name__ == '__main__':
	# Se define el puerto del sistema operativo que utilizará el servicio
	port = int(os.environ.get('PORT', 8086))
	# Se habilita la opción de 'debug' para visualizar los errores
	app.debug = True
	# Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
	app.run(host='0.0.0.0', port=port)
