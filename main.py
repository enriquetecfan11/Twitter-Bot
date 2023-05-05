import tweepy
import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()


# Configura las claves de acceso de la API de Twitter
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Autenticación con la API de Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# URL Tiempo
weather_api_url = 'https://api.openweathermap.org/data/2.5/weather'


# Función para obtener el clima actual
def get_current_weather(location):
    # Parámetros de la consulta
    params = {'q': location, 'appid': os.getenv('WEATHER_API_KEY'), 'units': 'metric'}

    response = requests.get(weather_api_url, params=params)

    weather_data = json.loads(response.text)

    print(f"El clima actual en {location} es de {weather_data['main']['temp']} grados Celsius y {weather_data['weather'][0]['description']}")

    return weather_data

# Ejemplo de uso
print(get_current_weather('Madrid, ES'))

# Función para enviar un tweet con la información del clima
def send_tweet(location):
    # Obtener información del clima
    weather_data = get_current_weather(location)

    # Formatear el tweet
    tweet_text = f"El clima actual en {location} es de {weather_data['main']['temp']} grados Celsius y {weather_data['weather'][0]['description']}"

    # Publicar el tweet
    api.update_status(tweet_text)


# Bucle principal
while True:
    # Buscar tweets que mencionan al bot y responder a ellos
    # print("Esperando menciones....")

    mentions = api.mentions_timeline()
    #print(mentions)

    # Chek if one user or oder metion @TecfanBot
    for mention in mentions:
        if '@TecfanBot' in mention.text:
            # Obtener el nombre de usuario de la persona que nos mencionó
            screen_name = mention.user.screen_name

            # Obtener el texto del tweet donde nos mencionaron
            tweet_text = mention.text

            # Imprimimos el tweet donde nos mencionaron
            print(f"El usuario {screen_name} nos mencionó en el siguiente tweet: {tweet_text}")

            # Si el texto de la mencion pone "tiempo en"
            if 'tiempo en' in tweet_text:
                # Obtener la ubicación
                location = tweet_text.split('tiempo en')[1]

                # Coge la primera palabra y la las dos primeras letras de location
                location = location.split()[0]
                print(location)

                # Enviar un tweet con la información del clima
                send_tweet(location)

                # Responder al tweet
                api.update_status(f"Hola, @{screen_name}! Aquí tienes la información del clima en {location}!")

        time.sleep(60)  # Esperar 1 minuto antes de revisar las menciones nuevamente



