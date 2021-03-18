#Imagen base
FROM node:12-alpine
#Directorio de trabajo. Recordamos, que si no existe, se crea
WORKDIR /app
#Copiamos la carpeta actual en la carpeta del directorio de trabajo de la imagen
COPY . .
#Instalamos los paquetes necesarios en produccion para la APP0
RUN yarn install --production
#Comando para al arrancar el contenedor, lanzar la aplicación
CMD ["node", "src/index.js"]
