import socket


def session(in_data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('localhost', 8310))
    except ConnectionRefusedError:
        print("Server is down.")
        return "Error"
    sock.send(in_data.encode())
    data = sock.recv(1024)
    sock.close()
    try:
        return data.decode()
    except UnicodeDecodeError:
        return data