import socket
from serverside import pickle_file, Cuser, tcp_pickle # need to refactor from subproject
from passlib.hash import pbkdf2_sha256

host = 'localhost'
port = 8310
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize socket
sock.bind((host, port)) # bind port
sock.listen(1) # number of connection in one time
while True:
    conn, addr = sock.accept() # new sock, client addr
    print('Connected', addr)
    data = conn.recv(1024) # receive packets 1024 bytes length, decode
    if not data:
        break
    try:
        data = data.decode().split('\n') # разделение присланного пакета на элементы
    except ValueError:
        print('Client packet was suspicious')
        conn.send('data error'.encode())
    if data[2] == 'Log':
        user = pickle_file.fileload(data[0]) # загрузка данных о пользователе
        if user == 'No account': # если пользователя не существует
            conn.send(user.encode()) # отправляем ответ клиенту о том, что аккаунта не существует
        elif pbkdf2_sha256.verify(data[1], user.password): # если введенный пароль совпадает с хешем
            user.update_collection()
            pickle_file.filesave(user)
            conn.send(tcp_pickle.pack(user))  # send user object data back to user
        else:
            conn.send('Error'.encode()) # отправка ошибки
    elif data[2] == 'Reg':
        user = Cuser.User(data[0], str(pbkdf2_sha256.hash(data[1])))
        pickle_file.filesave(user, reg=True)
        conn.send('Account created. Use your credentials to log in'.encode())
    conn.close()
    print('Closed', addr)
