import socket

def session(in_data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    packetsize = 100000
    try:
        sock.connect(('localhost', 8310))
    except ConnectionRefusedError and ConnectionResetError:
        print("Server is down.")
        return "Error"
    sock.send(in_data.encode())
    data = sock.recv(packetsize)
    while True:
        l = sock.recv(packetsize)
        data += l
        if not l:
            break

    sock.close()
    try:
        return data.decode()
    except UnicodeDecodeError:
        return data
