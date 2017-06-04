class Song():
    def __init__(self, name):
        self.name = name
        if name.split('.')[-1] == 'wav':
            self.__price = 5
        else:
            self.__price = 1
        self.owned = False
        self.key = '' # in development

    def __str__(self):
        return self.name

    def get_price(self):
        return self.__price

    def set_price(self, new_price=0):
        if new_price.isInteger:
            self.__price = new_price
