from easygui import *
import re, client, tcp_pickle, random, Cuser, streamplay


def login_procedure():
    while True:
        msg = "Введите логин и пароль"
        title = "Авторизация"
        fieldNames = ["Логин", "Пароль"]
        fieldValues = multpasswordbox(msg, title, fieldNames) # отображения окон
        if fieldValues == None:
            exit()
        username, pwd = fieldValues[0], fieldValues[1]
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{3,}', pwd):
            msgbox("Неверный формат пароля")
            continue
        response = client.session(username + '\n' + pwd + '\nLog')
        if response == 'No account':
            choice = ynbox("Аккаунта не существует, создать новый?", title = title,
                  default_choice="[<F1>]Да", cancel_choice="[<F2>]Нет")
            if choice == True:
                response = client.session(username + '\n' + pwd + '\nReg')
                msgbox('Аккаунт создан. Авторизуйтесь для начала работы', title=title)
        elif response == 'Error':
            msgbox('Неверный пароль')
        else:
            try:
                return tcp_pickle.load(response)  # если данные о пользователе вернулись, продолжаем работу
            except TypeError:
                msgbox(response)


def download(): # синхронизация библиотек
    i = 0
    for song in username.collection:
        if song.owned == True:
            i += 1
            # сравнивать хеши на сервере
            response = client.session(username.get_sessionkey() + '\n' + song.name + '\nDownload') # скачиваем файлы
            try:
                f = open(song.name, 'x') # пробуем создать файл
                msgbox('Загрузка %s завершена' % song.name, title=title)
            except FileExistsError: # если файл существует
                f = open(song.name, 'r') # читаем его содержимое
                if not response.__hash__() == f.read().__hash__():
                    # если хеш-суммы скачанного файла и файла на диске не совпадают
                    f.close()
                    f = open(song.name, 'w') # открываем для перезаписывания файл
                    msgbox('Обновление %s завершено' % song.name, title=title)
                else: # если скачанный файл такой-же как на диске, ничего не делаем
                    continue
            f.write(response)
            if not playlist.__contains__(song.name):
                playlist.append(song.name)
            f.close()
    if i == 0:
        msgbox('Коллекция пуста', title=title)



username = login_procedure()
playlist = [song.name for song in username.collection if song.owned == True]
choices = ['Магазин', 'Личная коллекция', 'Информация об аккаунте','Сменить пользователя',]
facts = ['Это приложение написано за неделю', 'Любишь музыку - люби и DRM',
         'У программы есть репазитарий', 'Почему этим занимается девопс', 'Спасибо за пользование',
         'Скажи спасибо, что не в консоли', 'Организационный момент','Хвастунишка','I am feeling myself good']
title = 'Music Player'
button = buttonbox("Добро пожаловать, %s" %username.id, title = title, choices = choices)

while True:
    if button == choices[0]:
        button = 'Магазин музыки'
        choice = choicebox(msg=button,title=title,choices=username.get_collection().split('\n'))
        if choice == None:
            continue
        sname = choice.split(',')[0].strip('\'')
        response = client.session(username.get_sessionkey() + '\n' + sname + '\nBuy')
        if response == 'Error':
            msgbox('Недостаточно денег на счету либо песня куплена', title=title)
        else:
            msgbox('Песня \'%s\' успешно куплена\nНажмите ОК для начала загрузки\n' % sname, title=title)
            username = tcp_pickle.load(response)
            download()

    elif button == choices[1]:
        button = 'Список песен. Выберете файл и нажмите ОК для воспроизведения'
        download()
        if not len(playlist) == 0:
            sname = choicebox(msg=button,title=title,choices=playlist)
            if sname == 'Add more choices':
                msgbox('Посетите магазин', title=title)
                continue
            elif sname == None:
                continue
            msgbox('Воспроизведение начнётся в фоновом режиме.', title=title)
            streamplay.play(sname,username.get_sessionkey().encode('utf-8'), username.password)

    elif button == choices[2]:
        button = 'Информация об аккаунте\n____________________\n'
        msgbox(msg=button + '\n' + str(username), title=title)

    elif button == choices[3]:
        button = 'Действительно выйти?'
        choice = ynbox(button, title=title,
                       default_choice="[<F1>]Да", cancel_choice="[<F2>]Нет")
        if choice == True:
                username = login_procedure()
        else:
            continue
    elif button == None:
        exit()
    r_index = random.randrange(0, len(facts))
    button = buttonbox(facts[r_index], title = title, choices = choices)


# добавить шифрование файлов
# пересмотреть функционал прошлой версии вдруг чё забыл