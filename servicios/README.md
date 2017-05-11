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

## Procesador de Tweets y Comentarios de Twitter

FORMAT: 1A  
HOST:         

## Twitter Service [/api/v1/tweets{?t}]

+ Parameters
    + t - Corresponde al título de la película o serie de Netflix.

### Get Information [GET]

+ Response 200 (application/json)

        {
          "statuses": [
            {
              "coordinates": null,
              "favorited": false,
              "truncated": false,
              "created_at": "Mon Sep 24 03:35:21 +0000 2012",
              "id_str": "250075927172759552",
              "entities": {
                "urls": [
        
                ],
                "hashtags": [
                  {
                    "text": "freebandnames",
                    "indices": [
                      20,
                      34
                    ]
                  }
                ],
                "user_mentions": [
        
                ]
              },
              "in_reply_to_user_id_str": null,
              "contributors": null,
              "text": "Aggressive Ponytail #freebandnames",
              "metadata": {
                "iso_language_code": "en",
                "result_type": "recent"
              },
              "retweet_count": 0,
              "in_reply_to_status_id_str": null,
              "id": 250075927172759552,
              "geo": null,
              "retweeted": false,
              "in_reply_to_user_id": null,
              "place": null,
              "user": {
                "profile_sidebar_fill_color": "DDEEF6",
                "profile_sidebar_border_color": "C0DEED",
                "profile_background_tile": false,
                "name": "Sean Cummings",
                "profile_image_url": "http://a0.twimg.com/profile_images/2359746665/1v6zfgqo8g0d3mk7ii5s_normal.jpeg",
                "created_at": "Mon Apr 26 06:01:55 +0000 2010",
                "location": "LA, CA",
                "follow_request_sent": null,
                "profile_link_color": "0084B4",
                "is_translator": false,
                "id_str": "137238150",
                "entities": {
                  "url": {
                    "urls": [
                      {
                        "expanded_url": null,
                        "url": "",
                        "indices": [
                          0,
                          0
                        ]
                      }
                    ]
                  },
                  "description": {
                    "urls": [
        
                    ]
                  }
                },
                "default_profile": true,
                "contributors_enabled": false,
                "favourites_count": 0,
                "url": null,
                "profile_image_url_https": "https://si0.twimg.com/profile_images/2359746665/1v6zfgqo8g0d3mk7ii5s_normal.jpeg",
                "utc_offset": -28800,
                "id": 137238150,
                "profile_use_background_image": true,
                "listed_count": 2,
                "profile_text_color": "333333",
                "lang": "en",
                "followers_count": 70,
                "protected": false,
                "notifications": null,
                "profile_background_image_url_https": "https://si0.twimg.com/images/themes/theme1/bg.png",
                "profile_background_color": "C0DEED",
                "verified": false,
                "geo_enabled": true,
                "time_zone": "Pacific Time (US & Canada)",
                "description": "Born 330 Live 310",
                "default_profile_image": false,
                "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
                "statuses_count": 579,
                "friends_count": 110,
                "following": null,
                "show_all_inline_media": false,
                "screen_name": "sean_cummings"
              },
              "in_reply_to_screen_name": null,
              "source": "Twitter for Mac",
              "in_reply_to_status_id": null
            }
          ]
        }

+ Response 215 (text)

        {
            "errors":[
                {
                    "code":215,
                    "message":"Bad Authentication data."
                }
            ]
        }
        

## Analizador de sentimiento

FORMAT: 1A  
HOST: localhost:8086         

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

Ejemplo de uso: 
1. Abrir el navegador
1. Ingresar a https://uaz.cloud.tyk.io/content/api/v1/information?t=Stranger+Things
