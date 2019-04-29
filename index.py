# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import random
import timetable
import datetime

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
# 0 - имя директора, 1 - адрес школы, 2 - название урока, 3 - новости, 4 - класс урока
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
    reqSence = [0, 0, 0, 0, 0]
    classN = 9
    classL = 2
    weekDay = datetime.datetime.today().weekday()
    lessonN = 3
    i = -1
    
    for s in tokens :
        i = i + 1
        
        if s.startswith('директор') or s.startswith('директри') :
            reqSence[0] = reqSence[0] + 3
            continue

        if s.startswith('адрес') :
            reqSence[1] = reqSence[1] + 3
            continue
        
        if s.startswith('урок') :
            reqSence[2] = reqSence[2] + 3
            continue
            
        if s.startswith('имя') :
            reqSence[0] = reqSence[0] + 3
            continue
        
        if s.startswith('новост') :
            reqSence[3] = reqSence[3] + 5
            continue
    
        if s.startswith('зов') or s.startswith('зва') or s.startswith('называ') or s.startswith('велича') :
            reqSence[0] = reqSence[0] + 3
            continue
            
        if s.startswith('находит') or s.startswith('находят') or s.startswith('располо'):
            reqSence[1] = reqSence[1] + 3
            continue
            
        if s.startswith('как') :
            reqSence[0] = reqSence[0] + 2
            continue
        
        if s.startswith('кабинет') :
            reqSence[4] = reqSence[4] + 3
            continue

        if s.startswith('класс') :
            reqSence[4] = reqSence[4] + 3
            continue

        if s.startswith('какой') :
            reqSence[4] = reqSence[4] + 2
            reqSence[2] = reqSence[2] + 2
            continue
                        
        if s.startswith('каком') :
            reqSence[4] = reqSence[4] + 2
            continue

        if s.startswith('какие') :
            reqSence[3] = reqSence[3] + 2
            continue

        if s.startswith('кто') :
            reqSence[0] = reqSence[0] + 2
            continue
            
        if s.startswith('где') :
            reqSence[1] = reqSence[1] + 3
            reqSence[4] = reqSence[4] + 2
            continue

        if s.startswith('понедел') :
            weekday = 0
            continue

        if s.startswith('вторн') :
            weekday = 1
            continue

        if s.startswith('сред') :
            weekday = 2
            continue

        if s.startswith('четвер') :
            weekday = 3
            continue

        if s.startswith('пятниц') :
            weekday = 4
            continue

        if s.startswith('суббот') :
            weekday = 5
            continue

        if s.startswith('воскресен') :
            weekday = 6
            continue
        
        if s.startswith('позавчера') :
            weekday = datetime.datetime.today().weekday() - 2
            if weekday < 0: weekday = weekday + 6
            continue
         
        if s.startswith('вчера') :
            weekday = datetime.datetime.today().weekday() - 1
            if weekday < 0: weekday = weekday + 6
            continue
       
        if s.startswith('сегодня') :
            weekday = datetime.datetime.today().weekday()
            continue
        
        if s.startswith('завтра') :
            weekday = datetime.datetime.today().weekday() + 1
            if weekday > 6 : weekday = weekday - 6
            continue
        
        if s.startswith('послезавтра') :
            weekday = datetime.datetime.today().weekday() + 2
            if weekday > 6 : weekday = weekday - 6
            continue   
        
        if s.startswith('1') or s.startswith('перв'):
            reqSence[2] = reqSence[2] + 3
            reqSence[4] = reqSence[4] + 3           

            if i < len(tokens) and tokens[i + 1].startswith('урок') :
                lessonN = 1
                tokens[i + 1] = '!!!'
            else :
                if i > 0 and tokens[i - 1].startswith('урок') :
                    lessonN = 1
                else :
                    classN = 1
            continue         
        
        if s.startswith('2') or s.startswith('два') or s.startswith('втор') :
            reqSence[2] = reqSence[2] + 3
            reqSence[4] = reqSence[4] + 3           

           if i < len(tokens) and tokens[i + 1].startswith('урок') :
                lessonN = 2
                tokens[i + 1] = '!!!'
            else :
                if i > 0 and tokens[i - 1].startswith('урок') :
                    lessonN = 2
                else :
                    classN = 2
            continue         
                     
        if s.startswith('3') or s.startswith('три') or s.startswith('трет') :
            reqSence[2] = reqSence[2] + 3
            reqSence[4] = reqSence[4] + 3           

           if i < len(tokens) and tokens[i + 1].startswith('урок') :
                lessonN = 3
                tokens[i + 1] = '!!!'
            else :
                if i > 0 and tokens[i - 1].startswith('урок') :
                    lessonN = 3
                else :
                    classN = 3
            continue         
        
        if s.startswith('4') or s.startswith('четыр') or s.startswith('четверт') :
            reqSence[2] = reqSence[2] + 3
            reqSence[4] = reqSence[4] + 3           

           if i < len(tokens) and tokens[i + 1].startswith('урок') :
                lessonN = 4
                tokens[i + 1] = '!!!'
            else :
                if i > 0 and tokens[i - 1].startswith('урок') :
                    lessonN = 4
                else :
                    classN = 4
            continue         
          
        if s.startswith('9') or s.startswith('девят') :
            reqSence[2] = reqSence[2] + 3
            reqSence[4] = reqSence[4] + 3           

           if i < len(tokens) and tokens[i + 1].startswith('урок') :
                lessonN = 9
                tokens[i + 1] = '!!!'
            else :
                if i > 0 and tokens[i - 1].startswith('урок') :
                    lessonN = 9
                else :
                    classN = 9
            continue
        
#    return reqSence.index(max(reqSence))
    if max(reqSence) < 4 :
        return answ[2]
    else :
        token = classN * 100 + classL * 10 + weekDay
        ind = reqSence.index(max(reqSence))
        if ind == 2 :
           return timetable.get_lesson_name(token, lessonN)
        else :
            if ind == 3 :
                return get_news_header()
            else:
                if ind == 4 :
                    return timetable.get_lesson_classroom(token, lessonN)
                else :
                    return info[reqSence.index(max(reqSence))]
