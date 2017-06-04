'''
Created on 2012. 2. 19.
This module is for playing mp3 (limited) and wav formatted audio file
@author: John
'''
import pygame


def playmusic(soundfile):
    """Stream music with mixer.music module in blocking manner.
       This will stream the sound from disk while playing.
    """
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(1000)


def stopmusic():
    """stop currently playing music"""
    pygame.mixer.music.stop()


def getmixerargs():
    pygame.mixer.init()
    freq, size, chan = pygame.mixer.get_init()
    return freq, size, chan


def initMixer():
    BUFFER = 3072  # audio buffer size, number of samples since pygame 1.8.
    FREQ, SIZE, CHAN = getmixerargs()
    pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)


'''You definitely need test mp3 file (a.mp3 in example) in a directory, say under 'C:\\Temp'
   * To play wav format file instead of mp3,
      1) replace a.mp3 file with it, say 'a.wav'
      2) In try except clause below replace "playmusic()" with "playsound()"

try:
    initMixer()
    filename = 'serverside\\mus_library\\rave.wav'
    playmusic(filename)
    print('Playing %s' %filename.split('\\')[-1])
except KeyboardInterrupt:  # to stop playing, press "ctrl-c"
    stopmusic()
    print("Stopped playing")
except Exception:
    print("Unknown error")

print("File ended")
'''