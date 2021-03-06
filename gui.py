# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: gui.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco & Yonathan Mtz.
# Modificada por: Miles Durón, Saúl Ibarra, Angel, Antonio Ibarra, Jesús Montalvo
# Version: 2.0 Mayo 2017
# Descripción:
#
#   Este archivo define la interfaz gráfica del usuario. Recibe dos parámetros que posteriormente son enviados
#   a servicios que la interfaz utiliza.
#   
#   
#
#                                             gui.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Porporcionar la in-  | - Consume servicios    |
#           |          GUI          |    terfaz gráfica con la|   para proporcionar    |
#           |                       |    que el usuario hará  |   información al       |
#           |                       |    uso del sistema.     |   usuario.             |
#           +-----------------------+-------------------------+------------------------+
#
import os
from flask import Flask, render_template, request
import urllib, json
import requests

app = Flask (__name__)

@app.route("/")
def index():
	# Método que muestra el index del GUI
	return render_template("index.html")

@app.route("/information", methods=['GET'])
def movie_information():
	# Se obtienen los parámetros que nos permitirán realizar la consulta
	title = request.args.get("t")

	json_result = {}
	# Se busca informacion con el titulo de la pelicula
	json_result['omdb'] = omdb_information(title)
	# Se guardan Tweets en una DB
        urllib.urlopen("http://localhost:8085/api/v1/tweets?t=" + title)
	#Se analizan sentimientos de los tweets en db
	json_result['sentiment'] = sentiment_analysis()
 	# Se regresa el template de la interfaz gráfica predefinido así como los datos que deberá carga
	return render_template("status.html", result=json_result)

       
def omdb_information(title):
        # Este procedimiento recupera informacion de la pelicula buscando por el titulo
	#Se envía el titulo al servicio que obtiene información de OMDB
	url_omdb = urllib.urlopen("http://localhost:8084/api/v1/information?t=" + title)
	# Se lee la respuesta de OMDB
	json_omdb = url_omdb.read()
	# Se convierte en un JSON la respuesta leída
	omdb = json.loads(json_omdb)
	# Regresa el JSON al método principal
	return omdb

def sentiment_analysis():
        # se llama al servicio para analizar el sentimiento de los comentarios guardados en la db
	url_sentiment = urllib.urlopen("http://localhost:8086/api/v1/sentiment")
	# Se obtiene la estadistica de los comentarios (cuantos positivos, negativos, etc)
	json_sentiment = url_sentiment.read()
	# Se convierte en un JSON la respuesta leída
	sentiment = json.loads(json_sentiment)
	# Regresa el JSON a el método principal    
	return sentiment


if __name__ == '__main__':
	# Se define el puerto del sistema operativo que utilizará el Sistema de Procesamiento de Comentarios (SPC).
	port = int(os.environ.get('PORT', 8000))
	# Se habilita el modo debug para visualizar errores
	app.debug = True
	# Se ejecuta el GUI con un host definido cómo '0.0.0.0' para que pueda ser accedido desde cualquier IP
	app.run(host='0.0.0.0', port=port)
