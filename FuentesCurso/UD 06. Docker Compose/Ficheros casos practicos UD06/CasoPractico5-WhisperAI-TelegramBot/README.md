# Telegram bot para transcribir audio con Whisper AI (Whisper CPP)
Este proyecto es un bot de Telegram que te ayuda a transcribir notas de voz o archivos de audio a texto, usando Whisper CPP (implementación de Whisper AI).
No depende de otros servicios (es un servicio auto-alojado).
Este proyecto es un único archivo Python que se puede ejecutar de forma independiente y también, tiene una versión dockerizada para desplegarlo rápidamente.

Este programa está inspirado en proyectos como https://0xacab.org/viperey/telegram-bot-whisper-transcriber y https://github.com/altbert/Whatsapp_speech_to_text.

# Detalles sobre implementación

Este proyecto utiliza bibliotecas de Python como numpy,python_telegram_bot y whispercpp.
La librería whispercpp es un binding de Whisper CPP para Python disponible en https://github.com/aarnphm/whispercpp. 
La conversión de los archivos de audio se realiza con "ffmpeg". Todos los audios procesados en el servidor se borran cuando se procesan.

# Self-Hosting

Alojar este chatbot por ti mismo es bastante fácil. Solo necesitas seguir estos pasos:

### Generar un nuevo bot:

- Inicia una nueva conversación con el bot @BotFather.
- Escribe el comando /newbot. Establece un nombre y un nombre de usuario.
- Copia el Token que BotFather te dará.

#### Obtén las ID de los usuarios/grupos permitidos:

- Si quieres obtener el ID de un usuario:
    - Inicia una nueva conversación con @RawDataBot.
    - Envía un mensaje o reenvía un mensaje de cualquier usuario deseado.
    - Copia el valor del campo "id" (dentro de "from" que se encuentra dentro de "message"). 
    - Si es un usuario, debería ser una ID como: 1234567890
- Si quieres obtener el ID de un grupo:
    - Introduce a @RawDataBot en el grupo del que quieras obtener el ID.
    - Copia el valor de "id" dentro de "chat".
    - Si es un grupo debe llevar delante un menos, con una ID como: -1234567890

### Configura el bot:

- Clona este repositorio.

  ```
  git clone https://github.com/sergarb1/telegram-bot-whisper-cpp
  ```

- Edita las variables de entorno en .env:

  ```
  nano .env
  ```

  - Establece tu `TELEGRAM_BOT_TOKEN`.
  - Establece tus `ALLOWED_CHAT_IDS`  (ID de usuarios/grupos separados por comas). Establécelo en * para permitir a todos los usuarios/grupos.
  - Establece el `WHISPER_MODEL` (base, tiny, small, medium, large)
  - Establece `AUDIO_LANGUAGE` (Si lo dejas en auto detectará el idioma)

  ### Construye e inicia el bot: 

  Puedes iniciar el bot con este comando:

  ```
  docker compose up --build -d
  ```

# Lanzar el software sin Docker
### Configura el bot:

- Clona este repositorio.

  ```
  git clone https://github.com/sergarb1/telegram-bot-whisper-cpp
  ```

- Edita el fichero run.sh

  ```
  nano run.sh
  ```

  - Establece tu `TELEGRAM_BOT_TOKEN`.
  - Establece tus `ALLOWED_CHAT_IDS`  (ID de usuarios/grupos separados por comas). Establécelo en * para permitir a todos los usuarios/grupos.
  - Establece el `WHISPER_MODEL` 
  - Establece `AUDIO_LANGUAGE` (Si lo dejas en auto detectará el idioma)
- Instala dependencias del sistema:
  ```
  apt update && apt install python3 python3-pip ffmpeg curl -y
  ```
- Instala las depedencias de Python
  ```
  pip3 install -r requirements.txt
  ```
- Lanza run.sh:
  ```
  ./run.sh
  ```
  
# Detalles sobre implementación

A continuación comentamos unos detalles de implementación:
  - Este proyecto utiliza bibliotecas de Python como numpy,python_telegram_bot y whispercpp.
  - La biblioteca de Python whispercpp es un binding de Whisper CPP para Python disponible en https://github.com/aarnphm/whispercpp.
    - Por debajo, utiliza la biblioteca realizada en C++ que ofrece gran rendimiento. 
  - La conversión de los archivos de audio se realiza con "ffmpeg". 
  - Todos los audios procesados en el servidor se borran cuando se procesan.
