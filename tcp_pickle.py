import pickle


def load(in_data): # функция преобразования данных с сервера в объекты(десериализация)
    data = pickle.loads(in_data)
    return data
