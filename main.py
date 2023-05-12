import tweepy
import requests
import json
import os
from dotenv import load_dotenv
import logging
import time
import sys
import schedule
import functools


load_dotenv()
logging.basicConfig(filename="bot.log", level=logging.INFO)


# Configura las claves de acceso de la API de Twitter
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Autenticación con la API de Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# URL Tiempo
weather_api_url = "https://api.openweathermap.org/data/2.5/weather"


# Función para saber si el bot está vivo
def is_alive():
    # Enviamos un simple tweet: "Hola, estoy vivo. Son las (hora de España)"
    tweet = f"Hola, estoy vivo. Son las {time.strftime('%H:%M:%S')}"
    # Publicar el tweet
    api.update_status(status=tweet)
    logging.info(f"Tweet publicado: {tweet}")


# Función para obtener el clima actual
def get_current_weather(location):
    # Parámetros de la consulta
    params = {"q": location, "appid": os.getenv("WEATHER_API_KEY"), "units": "metric"}
    response = requests.get(weather_api_url, params=params)
    weather_data = response.json()

    # Obtener los datos del clima
    weather = weather_data["weather"][0]["description"]

    # Obtener los datos de la temperatura
    temp = weather_data["main"]["temp"]

    # Obtener los datos de la humedad
    humidity = weather_data["main"]["humidity"]

    # Obtener los datos de la presión
    pressure = weather_data["main"]["pressure"]

    # Obtener los datos de la velocidad del viento
    wind_speed = weather_data["wind"]["speed"]

    # Obtener los datos de la dirección del viento
    wind_direction = weather_data["wind"]["deg"]

    # Obtener los datos de la visibilidad
    visibility = weather_data["visibility"]

    # Mensaje para enviar
    sendMessage = f"El clima actual en {location} es de {temp} ºC y {weather}, la humedad es de {humidity} %, la presión es de {pressure} hPa, la velocidad del viento es de {wind_speed} m/s, la dirección del viento es de {wind_direction} grados, la visibilidad es de {visibility} m"
    print(sendMessage)

    return temp, humidity, pressure, wind_speed


# Función para enviar un tweet con la información del clima
def send_tweet(location):
    # Obtener información del clima
    temp, humidity, pressure, wind_speed = get_current_weather(location)

    # Formatear el tweet + la hora es UTC +2
    tweet_text = f"""El clima actual en {location} es de {temp} ºC, la humedad es de {humidity} %, la presión es de {pressure} hPa, la velocidad del viento es de {wind_speed} m/s y son las """ + time.strftime("%H:%M:%S")


    # Publicar el tweet
    api.update_status(tweet_text)
    print("Tweet enviado:", tweet_text)


# Función para responder a menciones y proporcionar información del clima
def respond_to_mentions():
    while True:
        mentions = api.mentions_timeline()
        for mention in mentions:
            # Verificar si el tweet ya ha sido respondido
            if mention.in_reply_to_status_id is not None:
                logging.info("Tweet ya respondido")
                continue

            # Si el tweet está marcado como me gusta, no se hace nada
            if mention.favorited:
                logging.info("Tweet ya marcado como me gusta")
                continue

            if "@tecfanbot" or "@TecfanBot" in mention.text.lower():
                # Obtener el nombre de usuario
                username = mention.user.screen_name

                # Obtener la localización
                location = mention.text.split("tiempo en ")[1]
                print(location)

                # Obtener información del clima
                temp = get_current_weather(location)

                # Formatear el tweet
                tweet_text = f""" Hola @{username} el clima actual en {location} es de {temp} ºC y son las """ + time.strftime("%H:%M:%S")

                # Publicar el tweet
                api.update_status(status=tweet_text, in_reply_to_status_id=mention.id)
                logging.info(f"Tweet publicado: {tweet_text}")

                # Marcar el tweet como me gusta
                api.create_favorite(mention.id)
                logging.info("Tweet marcado como me gusta")

                # Romper el bucle
                break



def send_tweet_wrapper():
    send_tweet("Madrid, ES")

if __name__ == "__main__":
    schedule.every().hour.do(send_tweet_wrapper)

    # Configurar el tiempo máximo de ejecución (1 minuto = 60 segundos)
    tiempo_maximo = 20  # Tiempo máximo en segundos
    tiempo_inicial = time.time()

    # Ejecutar el bot continuamente
    while True:
        schedule.run_pending()
        respond_to_mentions()

        # Verificar si ha pasado el tiempo máximo permitido
        tiempo_actual = time.time()

        tiempo_transcurrido = tiempo_actual - tiempo_inicial
        if tiempo_transcurrido > tiempo_maximo:
            break
