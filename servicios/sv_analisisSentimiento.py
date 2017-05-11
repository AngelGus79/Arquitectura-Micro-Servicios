# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: sv_analisisSentimiento.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Saul, Miles, Antonio, Jesus, Angel
# Version: 1.2 Mayo 2017
# Descripción:
#
#   Este archivo define el rol de un servicio. Su funcion principal es evaluar el sentimiento de comentarios de Twitter
#   
#   por mashape (https://japerk-text-processing.p.mashape.com/sentiment/')
#   
#
#                                        sv_information.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Ofrecer un JSON que  | - Utiliza el API de    |
#           |    Evaluador de       |    estadistica del      |   mashape de proce     |
#           |     sentimiento       |    numero de comentarios|   samiento de texto    |
#           |      de tweets        |    positivos, negativos |                        |
#           |                       |    neutros y total.     |                        |
#           +-----------------------+-------------------------+------------------------+
#
#Ejemplo de uso: Abrir navegador e ingresar a "http://localhost:8086/api/v1/sentiment"
#
import os, urllib, json, oauth2, settings_analisisSentimiento, requests, sqlite3, sys
sys.path.append(os.path.abspath('') + '/data')
from flask import Flask, abort, render_template, request


app = Flask (__name__)

@app.route("/api/v1/sentiment", methods=['GET'])
def get_information():
        # Conecta con la base de datos SQLite3
        connection = sqlite3.connect("/data/database.sqlite")
        # creo el objeto cursor
        cursor = connection.cursor()
        # Recupera comentarios de la base de datos
        comments = cursor.execute('select text from Tweets')
        # checa si hay comentarios
	if comments is not None:
                # Se crean estadisticas sobre los sentimientos de los comentarios
		statistic = createStatistic(comments)

                # Cierra la conexion con la base de datos
                connection.close()

                # devuelve un json de la estadistica
                return json.dumps(statistic, ensure_ascii=False)
        else:
                # Se devuelve un error 400 para indicar que el servicio no puede funcionar sin comments
		abort(400)


def createStatistic(comments):
        pos = 0
	neg = 0
	neu = 0
        total = 0
        # itera cada comentario de la lista de comentarios
        for c in comments:
                # evalua el sentimiento del comentario uno por uno
                evaluatedSentiment = evaluateSentiment(c)
                # cuenta y separa los comentarios si son positivos, negativos o neutrales
                if evaluatedSentiment['label'] == "pos":
	                pos += 1
	        elif evaluatedSentiment['label'] == "neg":
	                neg += 1
	        else:
	                neu += 1
                total += 1
        # crea un diccionario de las estadisticas de sentimiento de los comentarios
        statistic = {'pos': pos, 'neg': neg, 'neu': neu, 'tot': total, }
        
        return statistic

def evaluateSentiment(comment):
        # Se conecta a la api que analiza el sentimiento de los comentarios
        endpoint = 'https://japerk-text-processing.p.mashape.com/sentiment/'
	headers = {'X-Mashape-Key': settings_analisisSentimiento.MASHAPE_KEY,}
	payload = {'language': 'english', 'text': comment, }
	response = requests.post(endpoint, headers=headers, data=payload)
	return response.json()


if __name__ == '__main__':
	# Se define el puerto del sistema operativo que utilizará el servicio
	port = int(os.environ.get('PORT', 8086))
	# Se habilita la opción de 'debug' para visualizar los errores
	app.debug = True
	# Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
	app.run(host='0.0.0.0', port=port)
