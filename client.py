import socket
from easygui import enterbox, msgbox


ip = enterbox('Enter IP')


def session(in_data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    packetsize = 10000
    try:
        sock.connect((ip, 8310))
    except ConnectionRefusedError:
        sock.close()
        return "Server rejected connection"
    except ConnectionResetError:
        sock.close()
        return "Server closed connection"
    except TimeoutError:
        sock.close()
        return "Server timeout"
    except OSError:
        return "Wrong IP"

    sock.send(in_data.encode())
    data = sock.recv(packetsize)
    while True:
        try:
            l = sock.recv(packetsize)
            data += l
            if not l:
                break
        except ConnectionResetError:
            sock.close()
            return "Server closed connection"
    sock.close()
    if data == '':
        return 'Server did not send any data'
    try:
        return data.decode()
    except UnicodeDecodeError:
        return data
