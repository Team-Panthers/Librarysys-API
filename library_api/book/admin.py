from django.contrib import admin
from .models import Book,BookCopy
# Register your models here.


admin.site.register(Book)
admin.site.register(BookCopy)