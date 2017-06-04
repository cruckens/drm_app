import pickle

def filesave(data, reg=False): # функция сохранения профиля
    try:
        f = open(data.id + '.pickle', 'xb')
    except FileExistsError: # если файл уже существует
        if reg == False: # перезаписываем только в том случае, если пользователь был зарегестрирован ранее
            # защита, если клиент подменивает пакет
            f = open(data.id + '.pickle', 'wb')
        else:
            return False
    pickle.dump(data, f)
    f.close()
    return True

def fileload(id): # функция загрузки профиля
    try:
            f = open(id +'.pickle', 'rb')
            data = pickle.load(f)
            f.close()
            return data
    except FileNotFoundError:
        return 'No account'
