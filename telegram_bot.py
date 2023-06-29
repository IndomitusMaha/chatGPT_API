import telebot
import webbrowser

bot = telebot.TeleBot('6341190720:AAEmekg_0fO1OrQVplWEIJfSAsra6g9BHwU')


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


bot.polling(non_stop=True)