from django.shortcuts import render
from django.http import HttpResponse
from . models import Genre, Author, Book, BookInstance

# Create your views here.

def index(request):
    #return HttpResponse("Sveiki atvykę!")
    book_count = Book.objects.count()
    book_instance_count = BookInstance.objects.count()
    book_instance_available_count = BookInstance.objects.filter(status='a').count()
    author_count = Author.objects.count()

    context = {
        'book_count': book_count,
        'book_instance_count' : book_instance_count,
        'book_instance_available_count' : book_instance_available_count,
        'author_count' :  author_count,
        'genre_count' : Genre.objects.count()
    }

    return render(request, 'library/index.html', context)

def authors(request):
    return render(request, 'library/authors.html', {'authors': Author.objects.all()})