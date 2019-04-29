from time import gmtime, strftime

lessons = {}
lessons[920] = {
    'names': [
        "белоруский язык", "физическая культура", "русский язык", "английский язык", "математика", "химия", "биология",
    ],
    'classrooms': [
        "412", "большой зал", "208", "308.309", "405", "314", "306",
    ]
}

lessonTime  = {
    'begin': [
        "8:30", "9:25", "10:25", "11:25", "12:25", "13:25", "14:20", "15:20",
    ],
    'end': [
        "9:15", "10:10", "11:10", "12:10", "13:10", "14:10", "15:05", "16:05",
    ],
    'beginInt': [
        510, 565, 625, 685, 745, 805, 860, 920,
    ],
    'endInt': [
        555, 610, 670, 730, 790, 850, 905, 965,
    ],
}

def name_to_n_lesson(name, token):
    
    i = 0
    for s in lessons[token]['names'] :
        if s.startswith(name[:3]) :
            return i
        i = i + 1
    return -1


def name_to_n_lesson_add(name, nameAdd, token):
    
    i = 0
    for s in lessons[token]['names'] :
        sArr = s.split()
        if len(sArr) > 1 and sArr[0].startswith(name[:3]) and sArr[1].startswith(nameAdd[:3]) :
            return i
        i = i + 1
    return -1

def get_lesson_name(token, n):
    
    return lessons[token]['names'][n - 1]

def get_lesson_classroom(token, n):
    
    return lessons[token]['classrooms'][n - 1]

def get_lesson_start_time(n):
    
    return lessonTime['begin'][n - 1]

def get_lesson_end_time(n):
    
    return lessonTime['end'][n - 1]

def get_lesson_start_time_remains_def(n):
    
#    if lessonTime['beginInt'][n - 1] - time_to_int()
    return lessonTime['beginInt'][n - 1] - time_to_int()

def get_lesson_end_time_remains_def(n):
    
    return lessonTime['endInt'][n - 1] - time_to_int()

def get_lesson_start_time_remains():
    
    for i in range(8) :
        if lessonTime['beginInt'][i] - time_to_int() <= 45 and lessonTime['beginInt'][i] - time_to_int() > 0  :
            return lessonTime['beginInt'][i] - time_to_int()
        if i > 0 and lessonTime['beginInt'][i - 1] - time_to_int() > -15 :
            return lessonTime['beginInt'][i - 1] - time_to_int()
    return (-9999)

def get_lesson_end_time_remains():
    
    for i in range(8) :
        if lessonTime['endInt'][i] - time_to_int() <= 45 and lessonTime['endInt'][i] - time_to_int() > 0 :
            return lessonTime['endInt'][i] - time_to_int()
        if i > 0 and lessonTime['endInt'][i - 1] - time_to_int() > -15 :
            return lessonTime['endInt'][i - 1] - time_to_int()
    return (-9999)

def time_to_int() :
    
    return int(60 * (3 + int(strftime("%H", gmtime())))) + int(strftime("%M", gmtime()))

def int_to_time(n) :
    
    return str(n // 60) + ':' + str(n % 60)
