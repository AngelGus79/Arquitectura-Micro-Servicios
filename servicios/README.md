# Servicios
En esta carpeta se definen los servicios utilizados en la tarea 2 dentro del Sistema de Procesamiento de Comentarios (SPC). La especificación de los servicios se realizaron utilizando blueprint de Apiary.
Las especificaciones son las siguientes:

## Procesador de Comentarios de IMDb
  
FORMAT: 1A  
HOST: https://uaz.cloud.tyk.io/content

## Information Service [/api/v1/information{?t}]

+ Parameters
    + t - Corresponde al título de la película o serie de Netflix.

### Get Information [GET]

+ Response 200 (application/json)

        { 
            "neg": "Some text",
            "neu": "Some text", 
            "pos": "Some text",
            "tot": "Some text",
            "Runtime": "Some text",
            "Genre": "Some text",
            "Director": "Some text",
            "Writer": "Some text",
            "Actors": "Some text",
            "Plot": "Some text",
            "Language": "Some text",
            "Country": "Some text",
            "Awards": "Some text.",
            "Poster": "Some text",
            "Metascore": "Some text",
            "imdbRating": "Some text",
            "imdbVotes": "Some text",
            "imdbID": "Some text",
            "Type": "Some text",
            "totalSeasons": "Some text",
            "Response": "Some text"
        }

+ Response 400 (text)

        {
            "title": "Bad Request"
            "message": "The browser (or proxy) sent a request that this server could not understand."
        }

Ejemplo de uso: 
1. Abrir el navegador
1. Ingresar a https://uaz.cloud.tyk.io/content/api/v1/information?t=Stranger+Things


## Analizador de sentimiento

FORMAT: 1A  
HOST: http://localhost:8086  

## Servicio de análisis de sentimiento [/api/v1/sentiment]

Se obtiene el número de comentarios positivos, negativos, neutrales y total de la última película procesada por el procesador de tweets

+ Parameters
    + Sin parámetros

### Get Information [GET]

+ Response 200 (application/json)

        { 
            "neg": "Número de comentarios negativos",
            "neu": "Número de comentarios neutrales", 
            "pos": "Número de comentarios positivos",
            "tot": "Total de comentarios procesados"
        }

+ Response 400 (text)

        {
            "title": "Bad Request"
            "message": "The browser (or proxy) sent a request that this server could not understand."
        }

