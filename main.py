import client, tcp_pickle
#player.play('mus_library/rave.wav')


def login(): # функция "окна" логина
    while True:
        id = input('Login: ').lower() # запрос на ввод логина
        pwd = input('Password: ')
        response = client.session((id + '\n' + pwd + '\nLog')) # отправляем на сервер запрос
        if response == 'No account': # если на сервере нет аккаунта, запрос на регистрацию
            choice = input('No account was found. Create new? (y)')
            if choice == 'y' or choice == 'Y':
                response = client.session((id + '\n' + pwd + '\nReg')) # отправка запроса регистрации
                print(response) # вывод в консоль ответа сервера
            continue
        elif response == 'Error':
            continue
        else:
            return tcp_pickle.load(response) # если данные о пользователе вернулись, продолжаем работу


def menu_help():
    print('Welcome, %s! Menu guide:\n1 - See info\n2 - Watch collection\n3 - Buy song\nL - Login to another'
          ' account\n' % username.id)  # вывод меню

username = login()
menu_help()
while True:
    choice = input('%s> ' %username.id)
    if choice == '1':
        print(username)
    elif choice == '2':
        print(username.get_collection())
    elif choice == '3':
        sname = str(input('Type name of the song you want to buy: '))
        print(username.expand_collection(sname))
    elif choice == 'l' or choice == "L":
            username = login()
            menu_help()
    else:
        continue
