class Book:
    BookType = ('Hardcover', 'Paper Back', 'Ebook')

    @classmethod
    def getbookstype(cls):
        return cls.BookType
    
    def setTitle(self, newTitle):
        self.title = newTitle

    def __init__(self, title, booktype):
        self.title = title
        if (not booktype in Book.BookType):
            raise ValueError(f"{booktype} is not valid")
        else:
            self.booktype = booktype


print(Book.getbookstype())
b1 = Book('tilte 1', 'Hardcover')
b2 = Book("title 2", 'other')
print(b1.title)
b1.setTitle('other')
print(b1.title)


