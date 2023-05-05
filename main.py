import tweepy
import requests
import json
import os
from dotenv import load_dotenv
import logging
import time

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


# Función para obtener el clima actual
def get_current_weather(location):
    # Parámetros de la consulta
    params = {"q": location, "appid": os.getenv("WEATHER_API_KEY"), "units": "metric"}
    response = requests.get(weather_api_url, params=params)
    weather_data = json.loads(response.text)

    # Solo se envia la temperatura
    weather_send = weather_data["main"]["temp"]

    print("weather_send", weather_send, "ºC")
    return weather_send


# Función para enviar un tweet con la información del clima
def send_tweet(location):
    # Obtener información del clima
    weather_data = get_current_weather(location)

    # Formatear el tweet
    tweet_text = f"El clima actual en {location} es de {weather_data['main']['temp']} grados Celsius y {weather_data['weather'][0]['description']}"

    # Publicar el tweet
    api.update_status(tweet_text)


def chek_mentions():
    while True:
        mentions = api.mentions_timeline()
        for mention in mentions:
            # print(mention.text, mention.user.screen_name)

            # Verificar si el tweet ya ha sido respondido
            if mention.in_reply_to_status_id is not None:
                logging.info("Tweet ya respondido")
                # print("Tweet ya respondido")
                break

            # Si cualquier tweet esta marcado como me gusta no se hace nada
            if mention.favorited:
                logging.info("Tweet ya marcado como me gusta")
                # si el tweet esta marcado como me gusta sale del programa
                break
            if "@tecfanbot" or "@TecfanBot" in mention.text.lower():
                logging.info("Tiene una mencion")

                screen_name = mention.user.screen_name
                tweet_text = mention.text

                location = tweet_text.split("tiempo en ")[1].strip()
                print(location)

                # Obtener información del clima
                weather_data = get_current_weather(location)

                # Formatear el tweet
                tweet_text = f"@{screen_name} El clima actual en {location} es de {weather_data} ºC"

                # Publicar el tweet
                api.update_status(tweet_text)

                # Marca el tweet de la mencion como me gusta
                api.create_favorite(mention.id)

                logging.info("Se ha enviado un tweet")
                print("Se ha enviado un tweet")
                break


if __name__ == "__main__":
    # send_tweet('Madrid, ES') # Este envia tweets
    get_current_weather("Madrid")  # Este chekea las menciones

    chek_mentions()  # Este solo para las menciones
    time.sleep(10)
    chek_mentions()
