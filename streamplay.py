import pyaudio

from decrypt import *


def play(fname,key,pwd):
    pyaud = pyaudio.PyAudio()
    srate=44100
    stream = pyaud.open(format = pyaud.get_format_from_width(2),
                    channels = 2,
                    rate = srate,
                    output = True)

    cipher = AESCipher(key,pwd)
    file = open(fname, 'r')
    data = cipher.decrypt(file.read())
    stream.write(data)