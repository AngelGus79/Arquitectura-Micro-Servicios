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
#   Este archivo define el rol de un servicio. Su función general es obtener informacion de comentarios de twitter y guardarlos en una base de datos.
#   ('https://www.twitter.com/').
#   
#   
#
#                                        sv_tweets.py
#           +-----------------------+-------------------------+----------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades           |
#           +-----------------------+-------------------------+----------------------------+
#           |                       |  - Guardar comentarios  | - Utiliza el API de        |
#           |    Procesador de      | de twitter en una bd    |   Twitter                  | 
#           |    comentarios        |                         | - Guarda en una db         |
#           |     en Twitter        |                         |   los tweets y comentarios |
#           |                       |                         |   mas recientes de la serie|
#           |                       |                         |   o pelicula en cuestión.  |
#           |                       |                         |                            |
#           +-----------------------+-------------------------+----------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8085/api/v1/tweets?t=matrix movie
#
import os
import sys
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
                # Se obtienen tweets atraves de una API
                tweets = getTweets(title)
                # Se persisten los Tweets en la base de datos
                save_information(tweets['statuses'])
                # Si todo sale bien se manda un codigo 204, para indicar que se realizo satisfactoriamente
                return ('', 204)
        else:
                # Se devuelve un error 400 para indicar que el servicio no puede funcionar sin parámetro
                abort(400)

def getTweets(title):
        # Se conecta con el servicio de Twitter a través de su API
        url_search = oauth_req('https://api.twitter.com/1.1/search/tweets.json?q=' +
                               title + '&src=typd&lang=en',
                               settings_tweets.ACCESS_TOKEN,
                               settings_tweets.ACCESS_TOKEN_SECRET)

        # Se devuelven en json los tweets
        return json.loads(url_search)

def save_information(tweets):
        # Método que guarda los tweets en una db
        # Se verifica si hay tweets
        if tweets is not None:
                # Conecta con la base de datos SQLite3
                connection = sqlite3.connect(os.getcwd()+"/servicios/data/database.sqlite")
                # se crea el objeto cursor
                cursor = connection.cursor()
                # Se limpia la db de tweets previos
                cursor.execute("delete from Tweets")
                # se aceptan los cambios hechos en la db
                connection.commit()
                # inserta tweets en db
                for tweet in tweets:
                        # los valores a agregar se formatean en una tupla
                        formatedValues = formatValues(tweet)
                        # se insertan los valores en la db
                        cursor.execute('insert into Tweets ' +
                                       '(id, screen_name, text) ' +
                                       'values (?,?,?)',
                                       formatedValues)

                # se confirman los cambios hechos en la db
                connection.commit()
                # se cierra la db
                connection.close()
                # se envia el codigo 204 para confirmar que todo se realizo satisfactoriamente
                return (' ', 204)

        else:
                # Se devuelve un error 400 para indicar que el servicio no puede funcionar sin parámetro
                abort(400)


def formatValues(tweet):
        # se crea una tupla con los campos a insertar
        values = (tweet['id'],
                  tweet['user']['screen_name'],
                  tweet['text'])
        # se devuelven los valores en tupla
        return values

                
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
