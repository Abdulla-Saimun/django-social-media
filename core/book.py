class Book:
    def __init__(self, title, author, page, price):
        self.title = title
        self.author = author
        self.page = page
        self.price = price
        self.__secret = 'this is secret'
    
    def getPrice(self):
        if hasattr(self, "_discount"):
            return self.price - (self.price * self._discount)
        else:
            return self.price

    def setDiscount(self, amount):
        self._discount = amount

class Newspaper:
    def __init__(self, name, page, price):
        self.name = name
        self.page = page
        self.price = price
    def getNewspaperName(self):
        return self.name


b1 = Book('Mockingjay', 'suzana', '400', 59)
b2 = Book('Academic Writing', 'collings', '120', 20)
print(b2.getPrice())
b2.setDiscount(0.25)
print(b2.getPrice())
print(b2._Book__secret)

n1 = Newspaper('Prothom', 20, 12)
print(isinstance(n1, Newspaper))

