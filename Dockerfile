FROM python:3.9-alpine

WORKDIR /app

# Instalar cron
RUN apk add --no-cache dcron

# Instalar dependencias
RUN pip install tweepy requests python-dotenv

# Copiar archivos
COPY . .

# Agregar script de configuración cron
RUN echo "0 */2 * * * python /app/main.py >> /var/log/cron.log 2>&1" >> /etc/crontabs/root

# Cargar variables de entorno desde el archivo .env
ENV $(cat .env | xargs)

# Ejecutar cron en primer plano
CMD ["crond", "-f", "-d", "8"]
