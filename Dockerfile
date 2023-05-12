FROM alpine:latest

# Actualizamos la distro alpine y luego instalamos python3
RUN apk update && apk add --no-cache python3 python3-dev py3-pip build-base

# Instalar dependencias
RUN pip3 install tweepy requests python-dotenv

# Copiar archivos
WORKDIR /app
COPY . .

# Correr por primera vez el bot
RUN python3 /app/main.py

# Agregar script de configuración cron
RUN echo "*/15 * * * * python3 /app/main.py >> /var/log/cron.log 2>&1" >> /etc/crontabs/root

# Ejecutar cron en primer plano
CMD ["crond", "-f", "-d", "8"]
