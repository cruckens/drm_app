import client, tcp_pickle
import re
#player.play('mus_library/rave.wav')


def login(): # функция "окна" логина
    while True:
        id = input('Login: ').lower() # запрос на ввод логина
        pwd = input('Password: ')
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{3,}', pwd):
            print('Wrong password format. Try again')
            continue
        response = client.session(id + '\n' + pwd + '\nLog') # отправляем на сервер запрос
        if response == 'No account': # если на сервере нет аккаунта, запрос на регистрацию
            choice = input('No account was found. Create new? (y)')
            if choice == 'y' or choice == 'Y':
                response = client.session((id + '\n' + pwd + '\nReg')) # отправка запроса регистрации
                print(response) # вывод в консоль ответа сервера
            continue
        elif response == 'Error':
            print(response + '. Try again')
            continue
        else:
            try:
                return tcp_pickle.load(response) # если данные о пользователе вернулись, продолжаем работу
            except TypeError:
                print(response)
                continue


def menu_help():
    print('Welcome, %s! Menu guide:\n1 - See info\n2 - Visit music store'
          '\n3 - Buy song\n4 - Download collection'
          '\nL - Login to another account\n' % username.id)  # вывод меню

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
        if not username.get_collection().__contains__(sname):
            print('Song with such name does not exist')
            continue
        for song in username.collection:
            if song.name  == sname:
                response = client.session(username.get_sessionkey() + '\n' + sname + '\nBuy')
                if response == 'Error':
                    print('Something went wrong')
                else:
                    print('You have bought \'%s\'\nYou can download it now' % sname)
                    username = tcp_pickle.load(response)

    elif choice == 'l' or choice == "L":
            username = login()
            menu_help()
    elif choice == '4':
        if not username.get_collection().__contains__('owned: True'):
            print('You have not purchased any songs. Press 3 to buy anything')
        for song in username.collection:
            if song.owned == True:
                print('Downloading \'%s\'' %song.name)
                response = client.session(username.get_sessionkey() + '\nDownload')
                with open(song.name, 'wb') as f:
                    f.write(response)
        print('Owned songs successfully downloaded')
    else:
        continue