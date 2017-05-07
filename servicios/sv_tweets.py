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
import os
from flask import Flask, abort, render_template, request
import urllib, json
import oauth2
import settings_tweets
app = Flask (__name__)


@app.route("/api/v1/tweets")
def get_information():
	# Método que obtiene la información de IMDB acerca de un título en particular
	# Se lee el parámetro 't' que contiene el título de la película o serie que se va a consultar
	title = request.args.get("t")
	# Se verifica si el parámetro no esta vacío 
	if title is not None:
		# Se conecta con el servicio de IMDb a través de su API

		url_search = oauth_req('https://api.twitter.com/1.1/search/tweets.json?q='+title+'&src=typd',settings_tweets.ACCESS_TOKEN, settings_tweets.ACCESS_TOKEN_SECRET)
		# Se lee la respuesta de IMDb
		#json_search = url_search.read()
		# Se convierte en un JSON la respuesta recibida
		search = json.loads(url_search)
		# Se regresa el JSON de la respuesta
		return json.dumps(search)
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
