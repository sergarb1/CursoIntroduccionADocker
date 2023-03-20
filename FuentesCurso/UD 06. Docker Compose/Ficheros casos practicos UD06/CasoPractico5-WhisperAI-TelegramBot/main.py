#!/usr/bin/pytho

#Import whispercpp binding in Python https://github.com/aarnphm/whispercpp
from whispercpp import Whisper

#To use OS functions
import os
#To measure processing time
import time

#To print logs of service
import logging

#Library to work with Telegram Bots  python_telegram_bot
import telegram
from telegram import Update
from telegram.ext import MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Message
from telegram.ext.filters import MessageFilter

#To execute process inside system
import subprocess

#To randomize file names
import random


class FilterAllowedChats(MessageFilter):

    def __init__(self, allowed_chat_ids):
        super().__init__()
        self.allowed_chat_ids = allowed_chat_ids

    def filter(self, message: Message) -> bool:
        #It is to allow voice files or audio files
        is_voice = bool(message.voice) or bool(message.audio)
        chat_id = str(message.chat.id)
        is_allowed_user = chat_id in self.allowed_chat_ids
        is_allowed = is_voice and is_allowed_user
        return is_allowed


#Function to scape markdowns chars for Telegram Bot
async def escapeMarkdownChars(text: str) -> str:
    escaping_chars = ['_', '*', '[', ']', '(', ')', '~', '>', '+', '-', '=', '|', '{', '}', '.', '!']
    temporal = text
    for char in escaping_chars:
        temporal = temporal.replace(char, f"\\{char}")
    return temporal


#Handler to start bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Bot activated. From now, I will transcript audio notes and files from allowed chat IDs"
    )

#async funtion to clean up temp files
async def cleanUpTmpFiles(oggFilePath, wavFilePath):
    os.remove(oggFilePath)
    os.remove(wavFilePath)
    return

#async function to convert OGG to Wav mono 16khz ready to WhisperCPP
#To convert it, ffmpeg program is required
async def convertOggToWav(oggFilePath, wavFilePath):
    #Command to perform conversion from OGG to Wav
    commandoToConvert=['ffmpeg', '-i', oggFilePath,'-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000',wavFilePath]
    print(commandoToConvert)
    subprocess.call(commandoToConvert)
    
#To change
async def setTypingInChat(context, effectiveChatId):
    await context.bot.send_chat_action(chat_id=effectiveChatId, action=telegram.constants.ChatAction.TYPING)

#To change
async def convertToMarkdown(text, processingTime,audioLanguage):
    transcription = text.strip()
    markdownMessage = '''\
Language: {audioLanguage}
Processing time: {processingTime}s
Transcription: 
```
{transcription}
```
    '''.format(transcription=transcription, processingTime=int(processingTime),audioLanguage=audioLanguage)
    
    escapedMarkdownMessage = await escapeMarkdownChars(markdownMessage)
    return escapedMarkdownMessage

#Asyn function to Download Voice note/Audio file to tmp folder
async def downloadVoiceMessage(context, fileId, wavAudioPath, oggAudioPath):
    #Obtain reference to file in Telegram bot
    new_file = await context.bot.get_file(fileId)
    #Download OGG file to TMP Folder
    await new_file.download_to_drive(custom_path=oggAudioPath)
    #Conver file to Wav to be processed with WhisperCPP
    await convertOggToWav(oggAudioPath, wavAudioPath)

#Async function to recibe Wav file and transcript it using WhisperCPP
async def transcribeAudio(wavAudioPath):
    
    result=whisperAILoaded.transcribe_from_file(wavAudioPath)
    #Return trasncribed text
    return result

#Handler to process messages (voice notes and audio files)
async def processVoiceMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #We obtain effective chat ID from message
    effectiveChatId = update.effective_chat.id
    #We obtain message ID
    messageId = update.message.message_id
    #We make a comprobation to obtain data if it is
    # a voice note or and audio file
    if update.message.voice:
        fileUniqueId = update.message.voice.file_unique_id
        fileId = update.message.voice.file_id
    elif update.message.audio:
        fileUniqueId = update.message.audio.file_unique_id
        fileId = update.message.audio.file_id
    #Random number to randomize file name fron different paths  
    toRandomFile=str(random.randint(0,32000))
    oggAudioPath = os.path.join(tmpPath,f"{fileUniqueId+toRandomFile}.ogg")
    wavAudioPath = f"{oggAudioPath}.wav"

    try:
        #Obtain start time to measure processing time
        startTime = time.time()
        #Set typing in chat to inform message is procesing
        await setTypingInChat(context, effectiveChatId)
        #Download voice note or audio file
        await downloadVoiceMessage(context, fileId, wavAudioPath, oggAudioPath)
        result = await transcribeAudio(wavAudioPath)
        #Obtain time when transcription has ended and obtain total processing time
        finalTime = time.time()
        processingTime = (finalTime - startTime)

        responseMessage = await convertToMarkdown(result, processingTime, audioLanguage)
        await context.bot.send_message(
            chat_id=effectiveChatId, text=responseMessage, reply_to_message_id=messageId,
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
        )

    except Exception as e:
        #If there is an error, we reply with information about
        errorMessage = f"Error. Exception={e}"
        await context.bot.send_message(chat_id=effectiveChatId, text=errorMessage, reply_to_message_id=messageId)
        pass
    finally:
        await cleanUpTmpFiles(oggAudioPath, wavAudioPath)


#Obtain Bot Telegram Token from evironment
botTelgramToken = os.environ.get("TELEGRAM_BOT_TOKEN")
#Obtain chat IDs allowed from evironment
allowedChatIDs = os.environ.get("ALLOWED_CHAT_IDS", default="").split(",")
#Obtain wich folder use with tmp files from environment
tmpPath = os.environ.get("TMP_PATH", default="/tmp/telgramBotWhisperAi")
#Obtaing wich model use from evironment
whisperModel = os.environ.get("WHISPER_MODEL", default="small")
#Obtaing audioLanguage from evironment (if you use always the same, it can do it faster)
audioLanguage = os.environ.get("AUDIO_LANGUAGE", default="auto")


#We load model
logging.info("Loading model. This can take some time if model has not been loaded before")
whisperAILoaded = Whisper.from_pretrained(whisperModel)
#We set audio language
whisperAILoaded.params.with_language(audioLanguage)
logging.info("Model loaded!")

#Create TMP folder if it doesnt exists and raise error if there is a problem
try:
    if not(os.path.exists(tmpPath)):
       os.mkdir(tmpPath)
except:
    logging.info("Error, problem creating TMP Folder")
    exit()

#Logging info
logging.info("Bot starting")
# We build Telegram Bot
telegramBotWhisperAiApp = ApplicationBuilder().token(botTelgramToken).build()
# We build the Handler for Telegram bot
startHandler = CommandHandler('start', start)
#Temporaly commented
filterAllowedChats = FilterAllowedChats(allowedChatIDs)
#Handler for audio notes and audio files
audioMessageHandler = MessageHandler(filterAllowedChats, processVoiceMessage)

#We add handlers to our Telegram bot
telegramBotWhisperAiApp.add_handler(startHandler)
telegramBotWhisperAiApp.add_handler(audioMessageHandler)

#We start to run polling our bot
telegramBotWhisperAiApp.run_polling()
#Logging info
logging.info("Bot started")
