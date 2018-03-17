# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}
user_id_lib = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(request.json, response)


    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        t = [0]
        user_id_lib[user_id] = t
        res['response']['text'] = 'Привет! Ты первый раз, тебе надо добавить данные, введи твоё имя'
        return

    if req['request']['command'] and user_id_lib[user_id][0] == 0:
        t = [req['request']['command'], 0]
        user_id_lib[user_id] = t
        res['response']['text'] = 'А теперь ' + user_id_lib[user_id][0]+' веди свой номер автомобиля'
        return

    if req['request']['command'] and user_id_lib[user_id][1] == 0:
        p = req['request']['command']
        t = [user_id_lib[user_id][0], p, 0]
        user_id_lib[user_id] = t
        res['response']['text'] = 'C какой стороны у вас бак ' + user_id_lib[user_id][1]
        res['response']['buttons'] = [{'title': suggest, 'hide': True}for suggest in ['слева', 'справа']]
        return

    if req['request']['command'] and user_id_lib[user_id][2] == 0:
        p = req['request']['command']
        if p == 'слева':
            p = 1
        else:
            p = 2
        res['response']['text'] = p
        t = [user_id_lib[user_id][0], user_id_lib[user_id][1], p, 0]
        user_id_lib[user_id] = t
        res['response']['text'] = 'у вас есть наша карта лояльности?'
        return

    '''if req['request']['command'] and user_id_lib[user_id][2] == 0:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        p = req['request']['command'] in 
        t = [user_id_lib[user_id][0], user_id_lib[user_id][1],p, 0]
        user_id_lib[user_id] = t
        res['response']['text'] = 'C какой стороны у тебя бак'
        # res['response']['buttons'] = getSuggests(user_id)
        return'''

    # Обрабатываем ответ пользователя.
    '''if req['request']['command'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
        req['request']['command']
    )
    res['response']['buttons'] = getSuggests(user_id)'''


# Функция возвращает две подсказки для ответа.
def getSuggests(user_id):
    #session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests
