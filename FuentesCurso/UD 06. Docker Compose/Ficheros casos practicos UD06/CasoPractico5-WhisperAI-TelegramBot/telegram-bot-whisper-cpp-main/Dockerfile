FROM ubuntu:22.10

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg git python3 python3-pip curl && apt-get autoremove -y && apt-get clean
WORKDIR /root
RUN git clone https://github.com/sergarb1/telegram-bot-whisper-cpp
WORKDIR /root/telegram-bot-whisper-cpp
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3","/root/telegram-bot-whisper-cpp/main.py"]

