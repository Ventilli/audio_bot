from telebot.types import Message
import speech_recognition as SR
import telegramApi
import subprocess
import requests
import telebot
import time
import os



TOKEN = '7161395864:AAHmQxVjFNwDsTRIxHIM8O0RugndRtcY3YA'
BOT = telebot.TeleBot(token = TOKEN)



def audio(message_path):
    audio = SR.AudioFile(message_path)
    recog = SR.Recognizer()
    with audio as source:
        data = recog.record(source)

    try:
        text = recog.recognize_google(data, language='ru_RU')
        return "В сообщении сказано: " + '"' + text + '"'
    except SR.UnknownValueError:
        return "Извините, не удалось распознать речь."
    except SR.RequestError as e:
        return "Ошибка сервиса распознавания речи; {0}".format(e)



@BOT.message_handler(commands=['start'])
def welcome(message:Message):
    if message.chat.username != None:
        BOT.reply_to(message,
                     f'Привет, {message.chat.username}! Отправь мне аудио сообщение и я переформатирую его в текст!\nУчти, что я работаю только с русским языком (пока)!')
    else:
        BOT.reply_to(message,
                     f'Привет! Отправь мне аудио сообщение и я переформатирую его в текст!\nУчти, что я работаю только с русским языком (пока)!')
    
    print(message.chat.username)

@BOT.message_handler(content_types=['voice'])
def audio_formatting(message:Message):
    file_info = BOT.get_file(message.voice.file_id)
    path = file_info.file_path
    file_name = os.path.basename(path)
    downloaded_file = BOT.download_file(path)
    with open(file_name, 'wb') as f:
        f.write(downloaded_file)

    print(file_name)
    time.sleep(1)
    subprocess.run(['ffmpeg', '-i', file_name, file_name+'.wav', '-y'])
    BOT.reply_to(message, format(audio(file_name+'.wav')))

# r = SR.Recognizer()


# mic = SR.Microphone()

# with mic as source:
#     print("Говорите...")
#     audio = r.listen(source)


# try:
#     text = r.recognize_google(audio, language="ru")
#     print("Вы сказали: " + text)
# except SR.UnknownValueError:
#     print("Извините, не удалось распознать речь.")
# except SR.RequestError as e:
#     print("Ошибка сервиса распознавания речи; {0}".format(e))


BOT.polling()