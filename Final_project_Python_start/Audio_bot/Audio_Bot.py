from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import speech_recognition as SR
import subprocess
import telebot
import os



# TOKEN = '7161395864:AAHmQxVjFNwDsTRIxHIM8O0RugndRtcY3YA'
TOKEN = '7227162273:AAEqAvDOER2NbBuidyc5KMogF-X8zf8h82g'
BOT = telebot.TeleBot(token = TOKEN)

userLanguage = 'ru_RU'



def audio(message_path):
    audio = SR.AudioFile(message_path)
    recog = SR.Recognizer()
    with audio as source:
        data = recog.record(source)

    try:
        text = recog.recognize_google(data, language = userLanguage)
        return "В сообщении сказано: " + '"' + text + '"'
    except SR.UnknownValueError:
        return "Извините, не удалось распознать речь."
    except SR.RequestError as e:
        return "Ошибка сервиса распознавания речи; {0}".format(e)

@BOT.message_handler(commands=['start'])
def welcome(message:Message):
    if message.chat.username != None:
        BOT.reply_to(message,
                     f"Привет, {message.chat.username}! Отправь мне аудио сообщение и я переформатирую его в текст!\nТы можешь изменить язык сообщения с помощью команды /change\n\n" +
                     f"Hi, {message.chat.username}! Send me an audio message and I'll reformat it into text!\nYou can change the language of the message using the /change command")
    else:
        BOT.reply_to(message,
                     "Привет! Отправь мне аудио сообщение и я переформатирую его в текст!\nТы можешь изменить язык сообщения с помощью команды /change\n\n" +
                     "Hi! Send me an audio message and I'll reformat it into text!\nYou can change the language of the message using the /change command")

@BOT.message_handler(commands=['change'])
def languageChoose(message:Message):
    markup = InlineKeyboardMarkup(row_width=2)
    ru = InlineKeyboardButton('Russian\nРусский', callback_data='ru')
    en = InlineKeyboardButton('English\nАнглийский', callback_data = 'en')
    markup.add(ru, en)
    BOT.send_message(message.chat.id, 'Для начала выбери язык сообщения\nFirst, select the language of the message',
                    reply_markup=markup)



@BOT.message_handler(content_types=['voice'])
def voice_formatting(message:Message):
    file_info = BOT.get_file(message.voice.file_id)
    path = file_info.file_path
    file_name = os.path.basename(path)
    downloaded_file = BOT.download_file(path)
    with open(file_name, 'wb') as f:
        f.write(downloaded_file)

    result = file_name.split('.')[0]
    process = subprocess.run(['ffmpeg', '-i', file_name, result+'.wav', '-y'])
    process
    print(result+'.wav')
    BOT.reply_to(message, format(audio(result+'.wav')))
    os.remove(result+'.wav')
    os.remove(file_name)

@BOT.message_handler(content_types=['audio'])
def audio_formatting(message:Message):
    file_info = BOT.get_file(message.audio.file_id)
    path = file_info.file_path
    file_name = os.path.basename(path)
    downloaded_file = BOT.download_file(path)
    with open(file_name, 'wb') as f:
        f.write(downloaded_file)

    result = file_name.split('.')[0]
    process = subprocess.run(['ffmpeg', '-i', file_name, result+'.wav', '-y'])
    process
    print(result+'.wav')
    BOT.reply_to(message, format(audio(result+'.wav')))
    os.remove(result+'.wav')
    os.remove(file_name)




@BOT.callback_query_handler(func = lambda call : True)
def callback(call : Message):
    global userLanguage

    if call is not None:

        if call.data == 'ru':
            userLanguage = 'ru_RU'
            BOT.send_message(call.message.chat.id, 'Отлично, теперь ваш язык по умолчанию: русский\nGreat, now your default language is Russian')
        if call.data == 'en':
            userLanguage = 'en_EN'
            BOT.send_message(call.message.chat.id, 'Отлично, теперь ваш язык по умолчанию: английский\nGreat, now your default language is English')
            
    else:
        print('Молосольные огурчики')

BOT.polling()