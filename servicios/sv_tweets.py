# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: sv_tweets.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco & Yonathan Mtz.
# Modificada por: Miles Durón, Saúl Ibarra, Angel, Antonio Ibarra, Jesús Montalvo
# Version: 2.0 Mayo 2017
# Descripción:
#
#   Este archivo define el rol de un servicio. Su función general es porporcionar en un objeto JSON
#   información detallada acerca de los comentarios acerca de una pelicula o una serie en particular en la plataforma Twitter haciendo uso de su API
#   ('https://www.twitter.com/').
#   
#   
#
#                                        sv_tweets.py
#           +-----------------------+-------------------------+----------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades           |
#           +-----------------------+-------------------------+----------------------------+
#           |                       |  - Ofrecer un JSON que  | - Utiliza el API de        |
#           |    Procesador de      | contenga información    |   Twitter                  | 
#           |    comentarios        | detallada de los        | - Devuelve un JSON con     |
#           |     en Twitter        | comentarios acerca de   |   los tweets y comentarios |
#           |                       | una pelicula o serie    |   mas recientes de la serie|
#           |                       | en particular dentro de |   o pelicula en cuestión.  |
#           |                       | la plataforma Twitter   |                            |
#           +-----------------------+-------------------------+----------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8085/api/v1/tweets?t=matrix movie
#
import os
import sys
sys.path.append(os.path.abspath('') + '/data')
from Conexion import Conexion
from flask import Flask, abort, render_template, request
import urllib, json
import oauth2
import settings_tweets
import sqlite3
app = Flask (__name__)


@app.route("/api/v1/tweets", methods=['GET'])
def get_information():
	# Método que obtiene la información de Twitter acerca de un título en particular
	# Se lee el parámetro 't' que contiene el título de la película o serie que se va a buscar
	title = request.args.get("t")
	# Se verifica si el parámetro no esta vacío 
	if title is not None:
		# Se conecta con el servicio de Twitter a través de su API
		url_search = oauth_req('https://api.twitter.com/1.1/search/tweets.json?q='+title+'&src=typd&lang=en',settings_tweets.ACCESS_TOKEN, settings_tweets.ACCESS_TOKEN_SECRET)
		# Se convierte en un JSON la respuesta recibida
		
		search = json.loads(url_search)
		tweets='{"tweets":['
		for tweet in search['statuses']:
			tweets+='{"id":' + str(tweet['id']) + ',"screen_name":"' + tweet['user']['screen_name']+ '","text":"'+tweet['text']+'"},'
		else:
			tweets=tweets[:-1]
			tweets+=']}'

		# Se regresa el JSON de la respuesta
		json_tweets=json.loads(tweets,strict=False)
		return json.dumps(json_tweets)
	else:
		# Se devuelve un error 400 para indicar que el servicio no puede funcionar sin parámetro
		abort(400)

@app.route("/api/v1/tweets", methods=['POST'])
def save_information():
	# Método que obtiene la información de Twitter acerca de un título en particular
	# Se lee el parámetro 't' que contiene el título de la película o serie que se va a buscar
	tweets = request.get_json()
	# Se verifica si el parámetro no esta vacío 
	if tweets['tweets'] is not None:
		try:
			con = Conexion()
			insert=('INSERT INTO Tweets Values')
			for tweet in tweets['tweets']:
				insert+='(' + str(tweet['id']) + ',"' + tweet['screen_name']+ '","'+tweet['text']+'"),'
			else:
				insert=insert[:-1]
			con.connect()
			comments=con.execute(insert)
			con.close()
		except sqlite3.Error as error:
			print 'An error occurred:', error.args[0]
		return json.dumps({"code":201}), 201
	else:
		# Se devuelve un error 400 para indicar que el servicio no puede funcionar sin parámetro
		abort(400)

def oauth_req(url, key, secret, http_method='GET', post_body='', http_headers=None):
    consumer = oauth2.Consumer(key=settings_tweets.CONSUMER_KEY, secret=settings_tweets.CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers )
    return content

if __name__ == '__main__':
	# Se define el puerto del sistema operativo que utilizará el servicio
	port = int(os.environ.get('PORT', 8085))
	# Se habilita la opción de 'debug' para visualizar los errores
	app.debug = True
	# Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
	app.run(host='0.0.0.0', port=port)
