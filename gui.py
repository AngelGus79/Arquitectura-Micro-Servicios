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
	# Se llena el JSON que se enviará a la interfaz gráfica para mostrársela al usuario
	json_result = {}
	# Se pasa el titulo al método que consume el servicio de OMDB
	json_result['omdb'] = omdb_information(title)
	# Se pasa el titulo y el tipo de contenido al método que consume el servicio de Twitter
	json_result['tweets'] = tweets_information(json_result['omdb']['Title'],json_result['omdb']['Type'])
	store_tweets(json_result['tweets'])
	"""text=[]
	for var in json_result['tweets']:
		text.append(var['text'])
	json_result['text']=text"""
        
	#json_result['sentiment'] = sentiment_analysis(text)
	json_result['sentiment'] = sentiment_analysis(json_result['omdb']['Title'])

	# Se regresa el template de la interfaz gráfica predefinido así como los datos que deberá cargar
	return render_template("status.html", result=json_result)

def omdb_information(title):
	#Se envía el titulo al servicio que obtiene información de OMDB
	url_omdb = urllib.urlopen("http://localhost:8084/api/v1/information?t=" + title)
	# Se lee la respuesta de OMDB
	json_omdb = url_omdb.read()
	# Se convierte en un JSON la respuesta leída
	omdb = json.loads(json_omdb)
	# Regresa el JSON al método principal
	return omdb

def sentiment_analysis(title):
	#url_omdb = urllib.urlopen("https://uaz.cloud.tyk.io/content/api/v1/information?t=" + title)
	#url_sentiment = requests.post("http://localhost:8086/api/v1/sentiment", json={'comments': comments})
	url_sentiment = urllib.urlopen("http://localhost:8086/api/v1/sentiment?t=" + title)
	# Se lee la respuesta de Twitter
	json_sentiment = url_sentiment.read()
	# Se convierte en un JSON la respuesta leída
	sentiment = json.loads(json_sentiment)
	# Regresa el JSON a el método principal
        
	return sentiment

def tweets_information(title,content_type):
	#Se envía el titulo y el tipo de contenido al servicio que obtiene información de Twitter
	url_search = urllib.urlopen("http://localhost:8085/api/v1/tweets?t=" + title + " " + content_type)
	# Se lee la respuesta de Twitter
	json_search = url_search.read()
	# Se convierte en un JSON la respuesta leída
	search = json.loads(json_search)
	# Regresa solo la parte del JSON donde se almacena la informacion de los tweets
	return search['tweets']

def store_tweets(tweets):
	url_store= requests.post("http://localhost:8085/api/v1/tweets", json={'tweets': tweets})
	# Se lee la respuesta de OMDB
	store = url_store.json()
	# Se convierte en un JSON la respuesta leída
	#sentiment = url_sentiment.json()
	# Regresa el JSON a el método principal
        
	return store

if __name__ == '__main__':
	# Se define el puerto del sistema operativo que utilizará el Sistema de Procesamiento de Comentarios (SPC).
	port = int(os.environ.get('PORT', 8000))
	# Se habilita el modo debug para visualizar errores
	app.debug = True
	# Se ejecuta el GUI con un host definido cómo '0.0.0.0' para que pueda ser accedido desde cualquier IP
	app.run(host='0.0.0.0', port=port)
