from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
import uuid

# Create your models here.

class Genre(models.Model):
    name = models.CharField(_('name'), max_length=200, help_text='Enter name of book genre')
    
    def __str__(self) -> str:
        return self.name

    def link_filtered_books(self):
        link = reverse('books')+ '?genre_id='+str(self.id)
        return format_html('<a class="genre" href="{link}">{name}</a>', link=link, name=self)

# Importavome modelių paketą
# Sukūrėme klasę (models.Model)
# Nurodėme, kad žanro pavadinimas bus iki 200 eilučių string'as, pagalbinį tekstą, kuris matysis administratoriaus svetainėje.
# def str nurodėme, kaip reprezentuosis modelis.        
# pridėkime knygos autorių:

class Author(models.Model):
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)

    def display_books(self) ->str:
        return ', '.join(book.title for book in self.books.all())
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    display_books.short_description = _('books')

    def link(self) -> str:
        link = reverse('author', kwargs={'author_id':self.id})
        return format_html('<a href="{link}">{author}</a>', link=link, author=self.__str__())

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Book(models.Model):
    title = models.CharField(_('title'), max_length=255) #reikia nurodyti ilgi
    summary = HTMLField(_('summary')) 
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True, 
        help_text=_('<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN code</a> consisting of 13 symbols'))
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    
    #protect - neleidzia istrinti autoriaus jei turi knygu (saugiausias)
    #set null - visas knygas kurios turi ta autoriu paliks be autoriaus 
    #cascade trinant autoriu istrins ir knygas (daznai naudojamas)
    #do nothing - ismes klaida bandant trinti (nerekomenduojama)
    genre = models.ManyToManyField(Genre, help_text=_('Choose genre(s) for this book'), verbose_name=_('genre(s)'))
    cover = models.ImageField("cover", upload_to='covers', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.author} - {self.title}"

    def display_genre(self) -> str:
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'genre(s)'


class BookInstance(models.Model):
    unique_id = models.UUIDField(_('unique ID'), default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, verbose_name="book", on_delete=models.CASCADE)
    due_back = models.DateField('due back', null=True, blank=True)

    LOAN_STATUS = (
        ('m', _("managed")),
        ('t', _("taken")),
        ('a', _("avalaible")),
        ('r', _("reserved")),
    )

    status = models.CharField('status', max_length=1, choices=LOAN_STATUS, default='m')
    reader = models.ForeignKey(get_user_model(), verbose_name="reader", on_delete=models.SET_NULL, null=True, blank=True, related_name='taken_noobs')

    @property
    def is_overdue(self):
        if self.due_back and self.due_back < datetime.date(datetime.now()):
            return True
        return False
    

    def __str__(self) -> str:
        return f"{self.unique_id}: {self.book.title}"

    class Meta: #griezta aprasomoji klase
        ordering = ['due_back']


class BookReview(models.Model):
    book = models.ForeignKey(
        Book,
        verbose_name="book",
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    reader = models.ForeignKey(
        get_user_model(), 
        verbose_name="reader", 
        on_delete=models.CASCADE, 
        related_name='book_reviews',
    )
    created_at = models.DateField(_("created_at"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=10000)

    def __str__(self):
        return f"{self.reader} on {self.book} at {self.created_at}"

    class Meta:
        ordering = ('-created_at', )
