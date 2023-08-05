import telebot
import webbrowser
import json
import openai
import requests
from datetime import datetime
import os


with open('key.json') as f:
    data = json.load(f)
key = data['key']

openai.api_key = key

with open('telegram_key.json') as f:
    data = json.load(f)
telegram_key = data['key']

# bot = telebot.TeleBot({telegram_key})
bot = telebot.TeleBot(token=telegram_key)


def generate_response(text):
    response = openai.Completion.create(
        prompt=text,
        engine='text-davinci-003', #модель
        max_tokens=100, #количество токенов в ответе
        temperature=0.7, #отвечает за креативность желаемого ответа от 0 до 1 (0-очень прямой ответ, 1 - очень креативный)
        n=1, #количество ответов
        stop=None, #указывает каким словом должен заканчиваться ответ
        timeout=20
    )

    if response.choices[0].text:
        return response.choices[0].text.strip() # 0 это номер ответа в списке ответов
    else:
        return None


def generate_image(message):
    url = 'https://api.openai.com/v1/images/generations'

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }

    json_image = {"prompt": message}

    response = requests.post(url=url, headers=headers, json=json_image)

    return response



@bot.message_handler(commands=['start', 'main', 'hello'])
def main(message):
    bot.send_message(message.chat.id, f'Yo, {message.from_user.first_name}!')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://google.com')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>No help!</b> <em>Figure out yourself!</em> <u>Done!</u>', parse_mode='html')


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    timestamp = str(datetime.now().timestamp())
    chat_id = str(message.chat.id)
    filename = f'{chat_id}_{timestamp}'
    with open(f'audio/{filename}.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    file = open(f'audio/{filename}.ogg', 'rb')
    result = openai.Audio.transcribe(
        api_key=key,
        model='whisper-1',
        file=file,
        response_format='text'
    )
    file.close()
    os.remove(f'audio/{filename}.ogg')
    bot.reply_to(message, f'Transcription: {result}')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Yo, {message.from_user.first_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    elif 'image:' in message.text.lower():
        prompt_text = str(message.text.lower().split(':')[1])
        response = generate_image(prompt_text)
        if response.status_code == 200:
            result_json = response.json()
            link = result_json['data'][0]['url']
            # result_string = json.dumps(result_json)
            bot.send_photo(message.chat.id, link)
        else:
            bot.reply_to(message, f'Error: {response.text}')
    else:
        response = generate_response(message.text)
        bot.send_message(message.chat.id, f'{response}')


bot.polling(non_stop=True)