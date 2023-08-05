import openai
import requests
import json


with open('key.json') as f:
    data = json.load(f)
key = data['key']

file = open('audio.wav', 'rb')

result = openai.Audio.transcribe(
    api_key=key,
    model='whisper-1',
    file=file,
    response_format='text'
)

print(result)