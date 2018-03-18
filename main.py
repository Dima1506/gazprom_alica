# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import requests

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}
user_id_lib = {}
sesaian_id = {}
ras_nomer = ['а', 'в', 'е', 'к', 'м', 'о', 'р', 'с', 'т', 'у', 'х']
cost_water = [20, 30, 50]
toplivo = [40.50, 37.50, 39.80]

ls2 = ''
ft2 = ['']
lg = ['']
ft3 = ['']

# Задаем параметры приложения Flask.
@app.route("/", methods=['GET', 'POST'])
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


def NamberCar(st):
    p = st
    st = len(st)
    if (st == 8) or (st == 9):
        return 1
    else:
        return 1
t3 = ['0']

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
        res['response']['text'] = 'А теперь ' + user_id_lib[user_id][0] + ' введи свой номер автомобиля'
        return

    if req['request']['command'] and user_id_lib[user_id][1] == 0:
        p = req['request']['command']
        if NamberCar(p) == 1:
            t = [user_id_lib[user_id][0], p, 0]
            user_id_lib[user_id] = t
            res['response']['text'] = 'C какой стороны у вас бак '
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in ['слева', 'справа']]
        else:
            res['response']['text'] = 'Ой, а вы не правильно ввели номер машины '
        return

    if req['request']['command'] and user_id_lib[user_id][2] == 0:
        p = req['request']['command']
        if p == 'слева':
            p = 1
        elif p == 'справа':
            p = 2
        else:
            res['response']['text'] = 'Вы выбрали неправильный ответ, повторите попытку'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in ['слева', 'справа']]
            return
        res['response']['text'] = p
        t = [user_id_lib[user_id][0], user_id_lib[user_id][1], p, 0]
        user_id_lib[user_id] = t
        res['response']['text'] = 'У вас есть наша карта лояльности?'
        res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in ['да', 'нет']]
        return
    if req['request']['command'] and user_id_lib[user_id][3] == 0:
        p = req['request']['command']
        t = [user_id_lib[user_id][0], user_id_lib[user_id][1], user_id_lib[user_id][2], 0, 0]
        user_id_lib[user_id] = t
        if p == 'да':
            res['response']['text'] = 'Введите номер вашей карты'
            user_id_lib[user_id][3] = 1
        elif p == 'нет':
            res['response']['text'] = 'Спасибо за введенные данные!!' + ' Возможные команды: где заправиться'
            user_id_lib[user_id][3] = 2
        else:
            res['response']['text'] = 'Вы выбрали неправильный ответ, повторите попытку'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in ['да', 'нет']]
            return
        return
    if req['request']['command'] and user_id_lib[user_id][3] == 1:
        p = req['request']['command']
        t = [user_id_lib[user_id][0], user_id_lib[user_id][1], user_id_lib[user_id][2], p, 0]
        user_id_lib[user_id] = t
        res['response']['text'] = 'Спасибо за введенные данные!!' + ' Возможные команды: где заправиться'
        return
    if req['request']['command'] != 'где заправиться' and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 0:
        res['response'][
            'text'] = 'Вы выбрали неправильный ответ, повторите попытку' + ' Возможные команды: где заправиться'
        return
    if t3[0] == '0':
        r = requests.get(
            'https://maps.googleapis.com/maps/api/place/textsearch/json?query=gazpromneft+gas+station&radius=5000&language=ru&opennow&location=55.711319,37.595655&key=AIzaSyDMkPyS3cWd1qIDDXYQHSLJ4PrV6ILkgVw')
        tp = r.text
        par_json = json.loads(tp)
        ft2[0] = str(par_json['results'][0]['formatted_address'])
        ft3[0] = str(par_json['results'][1]['formatted_address'])
        t3[0] = '1'
        return
    if req['request']['command'] == 'где заправиться' and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 0:
        sesaian_id[req['session']['session_id']] = [0, 0, 0, 0]
        res['response']['text'] = 'На заправке газпром по ' + ft2[0] + ' происходит слив топлива, следующая заправка на ' + ft3[0] + '. Выберите топливо:'
        res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in ['95', '92', 'ДТ']]
        user_id_lib[user_id][4] = 1
        return
    if req['request']['command'] and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 1:
        st = 'Вы выбрали топливо ' + req['request']['command'] + '. Стоимость данного топлива '
        if req['request']['command'] == '95':
            st = st + str(toplivo[0])
            sesaian_id[req['session']['session_id']][0] = 0
        elif req['request']['command'] == '92':
            st = st + str(toplivo[1])
            sesaian_id[req['session']['session_id']][0] = 1
        elif req['request']['command'] == 'ДТ':
            st = st + str(toplivo[2])
            sesaian_id[req['session']['session_id']][0] = 2
        else:
            res['response']['text'] = 'Вы выбрали неправильный ответ, повторите попытку'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in ['95', '92', 'ДТ']]
            return

        sesaian_id[req['session']['session_id']][2] = req['request']['command']
        st = st + ' рублей. Сколько литров топлива вам нужно:'
        res['response']['text'] = st
        user_id_lib[user_id][4] = 2
        return
    if req['request']['command'] and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 2:
        sesaian_id[req['session']['session_id']][1] = req['request']['command']
        st = 'Вам нужно ' + req['request']['command'] + ' литров бензина ' + sesaian_id[req['session']['session_id']][2]
        ft = toplivo[sesaian_id[req['session']['session_id']][0]]
        ft2[0] = str(ft * int(sesaian_id[req['session']['session_id']][1]))
        sesaian_id[req['session']['session_id']][1] = ft2[0]
        st = st + '. Это будет стоить ' + ft2[0]
        st = st + ' рублей.'
        st = st + '              Хотите купить другую нашу продукцию?'
        res['response']['text'] = st
        res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in ['да', 'нет']]
        user_id_lib[user_id][4] = 3
        return
    if req['request']['command'] and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 3:
        if req['request']['command'] == 'да':
            res['response']['text'] = 'Выбитрите тип продукции:'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in
                                          ['ДрайвКафе', 'Магазин-Eда', 'Магазин-НеEда']]

        elif req['request']['command'] == 'нет':
            res['response']['text'] = 'Спасибо за покупки. С вас ' + sesaian_id[req['session']['session_id']][
                1] + ' рублей.'
        else:
            res['response']['text'] = 'Вы выбрали неправильный ответ, повторите попытку'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in ['да', 'нет']]
            return
        user_id_lib[user_id][4] = 4
        return
    if req['request']['command'] and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 4:
        if req['request']['command'] == 'ДрайвКафе':
            return
        elif req['request']['command'] == 'Магазин-Eда':
            res['response']['text'] = 'Выбирите какую продукцию вы хотите:'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in
                                          ['минеральная вода', 'кока-кола', 'пепси', 'сникерс']]
            user_id_lib[user_id][4] = 5
            return
        elif req['request']['command'] == 'Магазин-НеEда':
            return
        else:
            res['response']['text'] = 'Вы выбрали неправильный ответ, повторите попытку'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in
                                          ['ДрайвКафе', 'Магазин-Eда', 'Магазин-НеEда']]
            return
        user_id_lib[user_id][4] = 5
        return

    if req['request']['command'] and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 5:
        if req['request']['command'] == 'минеральная вода':
            res['response']['text'] = 'Какую воду вы хотите?'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in
                                          ['газированная', 'негазированная']]
            user_id_lib[user_id][4] = 6
            return
        elif req['request']['command'] == 'кока-кола':
            return
        elif req['request']['command'] == 'пепси':
            return
        elif req['request']['command'] == 'сникерс':
            return
        else:
            res['response']['text'] = 'Вы выбрали неправильный ответ, повторите попытку'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in
                                          ['ДрайвКафе', 'Магазин-Eда', 'Магазин-НеEда']]
            return
        user_id_lib[user_id][4] = 6
        return
    if req['request']['command'] and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 6:
        # ls2 = req['request']['command']
        if req['request']['command'] == 'газированная':
            res['response']['text'] = 'Какую объём воды вам нужен?'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in
                                          ['0.3', '0.5', '1']]
        elif req['request']['command'] == 'негазированная':
            res['response']['text'] = 'Какую объём воды вам нужен?'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in
                                          ['0.3', '0.5', '1']]
        else:
            res['response']['text'] = 'Вы выбрали неправильный ответ, повторите попытку'
            res['response']['text'] = 'Какую воду вы хотите?'
            res['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in
                                          ['газированная', 'негазированная']]
            return
        user_id_lib[user_id][4] = 7
        return
    if req['request']['command'] and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 7:
        res['response']['text'] = 'Сколько вам нужно?'
        sesaian_id[req['session']['session_id']][3] = req['request']['command']
        user_id_lib[user_id][4] = 8
        return
    if req['request']['command'] and user_id_lib[user_id][3] >= 2 and user_id_lib[user_id][4] == 8:
        tf = req['request']['command']
        st = ' У вас ' + tf + ' бутылки ' + ls2 + 'газированной менеральной воды по ' + str(
            sesaian_id[req['session']['session_id']][3])
        st = st + '. И того с вас: ' + sesaian_id[req['session']['session_id']][1] + ' + ' + str(
            int(tf) * cost_water[1]) + ' = '
        st = st + str(int(tf) * cost_water[1] + float(ft2[0]))
        st = st + '. На ваш телефон прийдет сообщение для оплаты. Спасибо, что выбрали нас'
        res['response']['text'] = st
        user_id_lib[user_id][4] = 9
        return
