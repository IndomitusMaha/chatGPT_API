import json
import openai

with open('key.json') as f:
    data = json.load(f)
key = data['key']

openai.api_key = key


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


res = generate_response('HI! What is your opinion on the Emperor of Mankind?')
print(res)