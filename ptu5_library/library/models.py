from django.db import models
import uuid

# Create your models here.

class Genre(models.Model):
    name = models.CharField('name', max_length=200, help_text='Enter name of book genre')
    
    def __str__(self) -> str:
        return self.name

# Importavome modelių paketą
# Sukūrėme klasę (models.Model)
# Nurodėme, kad žanro pavadinimas bus iki 200 eilučių string'as, pagalbinį tekstą, kuris matysis administratoriaus svetainėje.
# def str nurodėme, kaip reprezentuosis modelis.        
# pridėkime knygos autorių:

class Author(models.Model):
    first_name = models.CharField('first name', max_length=50)
    last_name = models.CharField('last name', max_length=50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']

class Book(models.Model):
    title = models.CharField('title', max_length=255) #reikia nurodyti ilgi
    summary = models.TextField('summary') #teksto ilgis gali buti bet koks (nebutina nurodyti - neribotas)
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True, 
        help_text='<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN code</a> consisting of 13 symbols')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    #protect - neleidzia istrinti autoriaus jei turi knygu (saugiausias)
    #set null - visas knygas kurios turi ta autoriu paliks be autoriaus 
    #cascade trinant autoriu istrins ir knygas (daznai naudojamas)
    #do nothing - ismes klaida bandant trinti (nerekomentuojama)
    genre = models.ManyToManyField(Genre, help_text='Choose genre(s) for this book', verbose_name='genre(s)')

    def __str__(self) -> str:
        return f"{self.author} - {self.title}"

    def display_genre(self) -> str:
        return ', '.join(genre.name for genre in self.genre.all()[:3])



class BookInstance(models.Model):
    unique_id = models.UUIDField('unique ID', default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, verbose_name="book", on_delete=models.CASCADE)
    due_back = models.DateField('due back', null=True, blank=True)

    LOAN_STATUS = (
        ('m', "managed"),
        ('t', "taken"),
        ('a', "avalaible"),
        ('r', "reserved"),
    )

    status = models.CharField('status', max_length=1, choices=LOAN_STATUS, default='m')
    #price = models.DecimalField(("price"), max_digits=18, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.unique_id}: {self.book.title}"

    class Meta:
        ordering = ['due_back']