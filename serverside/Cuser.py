from os import listdir
from os.path import isfile, join
from serverside import Csong
import random, string

class User():
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.__gold = 0
        self.__sessionkey = ''
        self.__collection = [Csong.Song(f) for f in listdir('mus_library') if isfile(join('mus_library', f))] # list of song objects

    def __str__(self):
        return "Person: %s\nGold: %d" % (self.id, self.__gold)

    def get_sessionkey(self):
        self.__sessionkey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                                    for _ in range(20))
        return self.__sessionkey

    def expand_collection(self, sname):
        for song in self.__collection:
            if song.name == sname and song.get_price() <= self.__gold:
                setattr(song, 'owned', True)
                self.__gold -= song.get_price()
                return True
            else:
                return False

    def update_collection(self):
        actualsongs = [file for file in listdir('mus_library') if isfile(join('mus_library', file))]
        oldsongs = [song.name for song in self.__collection]
        [self.__collection.append(Csong.Song(new)) for new in actualsongs if not oldsongs.__contains__(new)]
        [self.__collection.remove(old) for old in self.__collection if not actualsongs.__contains__(old.name)]
        # обновляем библиотеку(проверка на предмет новых песен в папке и удаление старых


    def get_collection(self):
        return "\n".join(i.name + ' - $' + str(i.get_price()) + ', owned: ' + str(i.owned) for i in self.__collection)

    def set_gold(self,amount):
        self.__gold = amount