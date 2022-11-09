from django.contrib import admin
from . import models


class BookInstanceInline(admin.TabularInline):
    model = models.BookInstance
    extra = 0
    readonly_fields = ('unique_id',)
    can_delete = False


class BookdAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = (BookInstanceInline, )


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    readonly_fields = ('unique_id', ) #tuple atskiriam per kableli
    search_fields = ('unique_id', 'book__title', 'book__author__last_name__exact')
    list_editable = ('status', 'due_back')

    fieldsets = (
        ('General', {'fields':('unique_id', 'book')}),
        ('Availability', {'fields':('status', 'due_back')})
    )
# Register your models here.
admin.site.register(models.Author)
admin.site.register(models.Genre)
admin.site.register(models.Book, BookdAdmin)
admin.site.register(models.BookInstance, BookInstanceAdmin)