from django.contrib import admin
from core.models import User, Author, Publisher, Rack, Library, Book, BookBorrow, BookCopy
# Register your models here.

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Rack)
admin.site.register(Library)
admin.site.register(Book)
admin.site.register(BookBorrow)
admin.site.register(BookCopy)