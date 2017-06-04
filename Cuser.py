from os import listdir
from os.path import isfile, join
import Csong
import random, string

class User():
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.__gold = 0
        self.__sessionkey = ''
        self.collection = [Csong.Song(f) for f in listdir('mus_library') if isfile(join('mus_library', f))] # list of song objects

    def __str__(self):
        return "Имя аккаунта: %s\nЗолота: %d\nПесен приобретено %d" \
               %(self.id, self.__gold,len([song for song in self.collection if song.owned == True]))

    def get_sessionkey(self):
        return str(self.__sessionkey)

    def set_sessionkey(self):
        self.__sessionkey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                                    for _ in range(8))

    def expand_collection(self, sname):
        for song in self.collection:
            if song.name == sname and song.get_price() <= self.__gold and song.owned == False:
                setattr(song, 'owned', True)
                self.__gold -= song.get_price()
                return True
        return False

    def update_collection(self):
        actualsongs = [file for file in listdir('mus_library') if isfile(join('mus_library', file))]
        oldsongs = [song.name for song in self.collection]
        [self.collection.append(Csong.Song(new)) for new in actualsongs if not oldsongs.__contains__(new)]
        [self.collection.remove(old) for old in self.collection if not actualsongs.__contains__(old.name)]
        # обновляем библиотеку(проверка на предмет новых песен в папке и удаление старых


    def get_collection(self):
        return "\n".join('\'' + i.name + '\', $' + str(i.get_price()) + ', owned: '
                         + str(i.owned) for i in self.collection)

    def set_gold(self,amount):
        self.__gold = amount