# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import random
import timetable
# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
# 0 - имя директора, 1 - адрес школы, 2 - название урока, 3 - новости
sessionStorage = {}
quest = ["Могу ли я вам помочь?","Не хотите услышать новости о школе?", "Чем же?"]
answ = ["Я вас слушаю", "1+1=2", "Я вас не понимаю"]
info = ["Лубинская Татьяна Фаиловна, держу в курсе", "ул. Дружбы 7a"]
questN = 1

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
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Хорошо", "Нет, спасибо", "Ясно", "Больше", 
            ],
            'quest' : 1
        }
        
        res['response']['text'] = "Здравствуйте. Я - голосовой помощник для учеников и гостей Гимназии № 2 г. Новополоцка, и я могу отвечать на ваши вопросы о ней, просто спросите. Для помощи по командам скажите ПОМОЩЬ."
        res['response']['tts'] = "Здравствуйте. Я - голосовой помощник для учеников и гостей Гимназии № 2 г. Новополоцка, и я могу отвечать на ваши вопросы о ней, просто спросите. Для помощи по командам скажите ПОМОЩЬ."
    
        return
    
    if req['request']['original_utterance'].lower() in [
        'помощь',
        'что ты умеешь',
        'что ты умеешь?',
    ]:

        res['response']['text'] = 'Я могу рассказать вам о школе : пока только её адрес и имя директора. Еще могу почитать новости, но только одну. Задавайте ваши вопросы, а я постараюсь ответить)' #TODO
        res['response']['tts'] = 'Я могу рассказать вам о школе : пока только её адрес и имя директора. Еще могу почитать новости, но только одну. Задавайте ваши вопросы, а я постараюсь ответить'
    
        return
    
    questN = sessionStorage[user_id]['quest']
    
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'давай',
        'хорошо',
        'да',
        'ok',
    ]:
        if questN == 1:
            res['response']['text'] = get_news_header()
            res['response']['tts'] = get_news_header()
        else :
            if questN == 0 :
                res['response']['text'] = quest[2]
                res['response']['tts'] = quest[2]
            else :
                res['response']['text'] = answ[questN];
                res['response']['tts'] = answ[questN];
        res['response']['buttons'] = get_suggests(user_id, (-1 * questN) - 1)
        return
    
    if req['request']['original_utterance'].lower() in [
        'еще',
        'больше',
    ]:
        if questN == 1:
            res['response']['text'] = get_news_full()
            res['response']['tts'] = get_news_full()
        return
    
    if req['request']['original_utterance'].lower() in [
        'no',
        'нет',
        'не надо',
    ]:
        questN = random.randint(0, 1)
        res['response']['text'] = quest[questN]
        res['response']['tts'] = quest[questN]
        res['response']['buttons'] = get_suggests(user_id, questN)
        sessionStorage[user_id]['quest'] = questN
        
        return
    
    if req['request']['original_utterance'].lower() in [
        'понятно',
        'спасибо',
        'ясно',
    ]:
        questN = random.randint(0, 1)
        res['response']['text'] = quest[questN]
        res['response']['tts'] = quest[questN]
        res['response']['buttons'] = get_suggests(user_id, questN)
        sessionStorage[user_id]['quest'] = questN
        
        return
        
    answ = get_req_sence(req['request']['nlu']['tokens'])
    res['response']['text'] = answ
    res['response']['tts'] = answ

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id, quest):
    session = sessionStorage[user_id]

    if quest == -1 :
        suggests = [
            {'title': suggest, 'hide': True}
            for suggest in session['suggests'][2:]
        ]
    else :
        if quest == -2 :
            suggests = [
                {'title': suggest, 'hide': True}
                for suggest in session['suggests'][2:]
            ]
        else :
            if quest == 0 :
                suggests = [
                    {'title': suggest, 'hide': True}
                    for suggest in session['suggests'][1]
                ]
            else :
                if quest == 1 :
                    suggests = [
                        {'title': suggest, 'hide': True}
                        for suggest in session['suggests'][:1]
                    ]
                else :
                    suggests = [
                        {'title': suggest, 'hide': True}
                        for suggest in session['suggests'][:1]
                    ]
                
    sessionStorage[user_id] = session

    return suggests

def get_news_header():
    
    return "20 декабря - единый день информирования"

def get_news_full():
    
    return "Для учащихся VIII - XI классов 20 декабря в 14.20 в актовом зале гимназии пройдёт единый день информирования \"Будущее Беларуси - это мы\" в рамках программы \"ШКОЛА АКТИВНОГО ГРАЖДАНИНА\""

def get_req_sence(tokens_or):
    tokens = tokens_or
    reqSence = [0, 0, 0, 0]
    classN = 9
    classL = 2
    weekDay = 1
    lessonN = 3
    i = -1
    
    for s in tokens :
        i = i + 1
        
        if s.lower() in [
            'директор',
            'директора',
            'директоре',
            'директору',
            'директрисса',
            'директриссу',
            'директриссе',
        ]:
            reqSence[0] = reqSence[0] + 3
            continue

        if s.lower() in [
            'адрес',
            'адреса',
            'адресе',
            'адресу',
        ]:
            reqSence[1] = reqSence[1] + 3
            continue
        
        if s.lower() in [
            'урок',
            'урока',
            'уроку',
            'уроке',
        ]:
            reqSence[2] = reqSence[2] + 3
            continue
            
        if s.lower() in [
            'имя',
            'имени',
            'именем',
        ]:
            reqSence[0] = reqSence[0] + 3
            continue
        
        if s.lower() in [
            'новости',
            'новостей',
            'новостях',
            'новостям',
        ]:
            reqSence[3] = reqSence[3] + 5
            continue
    
        if s.lower() in [
            'зовут',
            'звали',
            'звалу',
            'звать',
            'называть',
            'называю',
            'называли',
            'называют',
            'величать',
            'величаю',
            'величали',
            'величают',
        ]:
            reqSence[0] = reqSence[0] + 3
            continue
            
        if s.lower() in [
            'находится',
            'находился',
            'находятся',
            'находиться',
            'находился',
            'находяться',
            'расположена',
            'распологается',
            'распологалась',
        ]:
            reqSence[1] = reqSence[1] + 3
            continue
            
        if s.lower() in [
            'как',
        ]:
            reqSence[0] = reqSence[0] + 2
            continue
        
        if s.lower() in [
            'какой',
        ]:
            reqSence[2] = reqSence[2] + 2
            continue
                        
        if s.lower() in [
            'кто',
        ]:
            reqSence[0] = reqSence[0] + 2
            continue
            
        if s.lower() in [
            'где',
        ]:
            reqSence[1] = reqSence[1] + 2
            continue
         
        if s.lower() in [
            '3',
            '3-ый'
            '3-ого'
            '3-ом'
            '3-ому'
            '3ый'
            '3ого'
            '3ом'
            '3ому'
            'три'
            'третий'
            'третьего'
            'третьем'
            'третьему'
        ]:
            reqSence[2] = reqSence[2] + 3
            if i < len(tokens) and tokens[i + 1].lower() in [
                'урок',
                'урока',
                'уроку',
                'уроке', 
            ] :
                lessonN = 3
                tokens[i + 1] = '!!!'
            else :
                if i > 0 and tokens[i - 1].lower() in [
                    'урок',
                    'урока',
                    'уроку',
                    'уроке',  
                ] :
                    lessonN = 3
                else :
                    classN = 3
            continue         
         
        if s.lower() in [
            '9',
            '9-ый'
            '9-ого'
            '9-ом'
            '9-ому'
            '9ый'
            '9ого'
            '9ом'
            '9ому'
            'девять'
            'девятый'
            'девятого'
            'девятом'
            'девятому'
        ]:
            reqSence[2] = reqSence[2] + 3
            if i < len(tokens) and tokens[i + 1].lower() in [
                'урок',
                'урока',
                'уроку',
                'уроке', 
            ] :
                lessonN = 9
                tokens[i + 1] = '!!!'
            else :
                if i > 0 and tokens[i - 1].lower() in [
                    'урок',
                    'урока',
                    'уроку',
                    'уроке',  
                ] :
                    lessonN = 9
                else :
                    classN = 9
            continue
        
#    return reqSence.index(max(reqSence))
    if max(reqSence) < 4 :
        return answ[2]
    else :
        ind = reqSence.index(max(reqSence))
        if ind == 2 :
            token = classN * 100 + classL * 10 + weekDay
            return timetable.get_lesson_name(token, lessonN)
        else :
            if ind == 3 :
                return get_news_header()
            else :
                return info[reqSence.index(max(reqSence))]
