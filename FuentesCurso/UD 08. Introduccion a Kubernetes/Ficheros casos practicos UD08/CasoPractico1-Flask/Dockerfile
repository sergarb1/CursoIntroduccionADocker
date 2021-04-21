#Utilizamos la imagen con Python 3.7
FROM python:3.7
#Copiamos del anfitrion a la imagen la aplicación
COPY app.py /app.py
#Instalamos la biblioteca Flash
RUN pip install flask
#Exponemos el puerto 5000
EXPOSE 5000
#Indicamos que se ejecute la aplicación al iniciar el contenedor
ENTRYPOINT env FLASK_APP=app.py flask run --host=0.0.0.0