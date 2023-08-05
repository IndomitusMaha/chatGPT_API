import telebot
import webbrowser
import json
import openai
import requests

with open('key.json') as f:
    data = json.load(f)
key = data['key']

openai.api_key = key


def generate_image(message):
    url = 'https://api.openai.com/v1/images/generations'

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }

    json_image = {"prompt": message}

    response = requests.post(url=url, headers=headers, json=json_image)

    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print('Error: ', response.text)


message = 'Godzilla in bikini'
generate_image(message)
