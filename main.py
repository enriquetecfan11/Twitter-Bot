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

    # Solo se envia la temperatura
    weather_send = weather_data['main']['temp']

    print("weather_send", weather_send)
    return weather_send

    # print(f"El clima actual en {location} es de {weather_data['main']['temp']} grados Celsius y {weather_data['weather'][0]['description']}")

    # return weather_data


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
    # Buscar tweets que mencionan al bot y responder a ellos
    # print("Esperando menciones....")

    mentions = api.mentions_timeline()
    # Chek if one user or oder metion @TecfanBot
    for mention in mentions:
        print(mention.user.screen_name + mention.text)
        if '@TecfanBot' or '@tecfanbot' in mention.text:
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

                # Responder al tweet -> Hola @user, el tiempo en tu (location) es get_current_weather(location)
                api.update_status(f"Hola @{screen_name}, el tiempo en {location} es {get_current_weather(location)}")
                print(f"Tweet: ", f"Hola @{screen_name}, el tiempo en {location} es {get_current_weather(location)}" )

if __name__ == "__main__":
    chek_mentions() # Este solo para las menciones
    # send_tweet('Madrid, ES') # Este envia tweets
    get_current_weather('Madrid, ES') #Este chekea las menciones

