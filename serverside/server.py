import socket
import pickle_file, Cuser, tcp_pickle # need to refactor from subproject
from passlib.hash import pbkdf2_sha256
from os import listdir
from encrypt import *

host = '0.0.0.0'
port = 8310
packetsize = 10000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize socket
sock.bind((host, port)) # bind port
sock.listen(5) # number of connection in one time
users = [pickle_file.fileload(f.split('.pickle')[0]) for f in listdir() if f.endswith('.pickle')]

while True:
    conn, addr = sock.accept() # new sock, client addr
    print('Connected', addr)
    data = conn.recv(packetsize) # receive packets 1024 bytes length, decode
    if not data:
        break
    try:
        data = data.decode().split('\n') # разделение присланного пакета на элементы
    except ValueError:
        print('Client packet was suspicious')
        conn.send('data error'.encode())
    if data[-1] == 'Log':
        user = pickle_file.fileload(data[0]) # загрузка данных о пользователе
        if user == 'No account': # если пользователя не существует
            conn.send(user.encode()) # отправляем ответ клиенту о том, что аккаунта не существует
        elif pbkdf2_sha256.verify(data[1], user.password): # если введенный пароль совпадает с хешем
            user.update_collection() # получаем обновлённую коллекцию песен
            user.set_sessionkey() # устанавливаем сеансовый ключ
            pickle_file.filesave(user) # сохраняем состояние юзера
            conn.send(tcp_pickle.pack(user))  # send user object back to client
            users.append(user) # append list of users with those who were connecting since server is up
        else:
            conn.send('Error'.encode()) # отправка ошибки

    elif data[-1] == 'Reg':
        user = Cuser.User(data[0], str(pbkdf2_sha256.hash(data[1])))
        user.set_gold(20)
        pickle_file.filesave(user, reg=True)
        print('User \'%s\' created from %s' %(user.id,addr))
        conn.send('Account created. Use your credentials to log in'.encode())

    elif data[-1] == 'Buy':
        for user in users:
            if data[0] == user.get_sessionkey():
                if user.expand_collection(data[1]):
                    pickle_file.filesave(user)
                    conn.send(tcp_pickle.pack(user))
        conn.send('Error'.encode())

    elif data[-1] == 'Download':
        for user in users:
            if data[0] == user.get_sessionkey():
                for song in user.collection:
                    if song.owned == True and data[1] == song.name:
                        f = open('mus_library/' + song.name, 'rb')
                        cipher = AESCipher(user.get_sessionkey().encode('utf-8'), user.password)
                        print('Sending to %s file %s'%(addr,song.name))
                        l = cipher.encrypt(f.read()).encode()
                        f.close()
                        conn.sendall(l)
    conn.close()
    print('Closed', addr)
