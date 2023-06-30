import telebot
import webbrowser
import json
import openai

with open('key.json') as f:
    data = json.load(f)
key = data['key']

openai.api_key = key

with open('telegram_key.json') as f:
    data = json.load(f)
telegram_key = data['key']

bot = telebot.TeleBot({telegram_key})


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


@bot.message_handler(commands=['start', 'main', 'hello'])
def main(message):
    bot.send_message(message.chat.id, f'Yo, {message.from_user.first_name}!')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://google.com')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>No help!</b> <em>Figure out yourself!</em> <u>Done!</u>', parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Yo, {message.from_user.first_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    else:
        response = generate_response(message.text)
        bot.send_message(message.chat.id, f'{response}')


bot.polling(non_stop=True)