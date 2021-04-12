#Imagen base
FROM python:3
#Definimos la variable de entorno PYTHONBUFFERED
ENV PYTHONUNBUFFERED=1
#Establecemos como directorio de trabajo /code
WORKDIR /code
#Copiamos requirements.txt del anfitrión a la imagen
COPY requirements.txt /code/
#Instalamos las dependencias de Python indicadas en requirements
RUN pip install -r requirements.txt

