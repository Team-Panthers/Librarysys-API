from django.db import models
from django.contrib.auth.models import User

class Library(models.Model):
    no_of_rack = models.PositiveIntegerField()

    def __str__(self):
        return f"Library {self.library_id}"

class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title

class Rack(models.Model):
    number = models.AutoField(primary_key=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    book_copy = models.OneToOneField('BookCopy', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"Rack {self.rack_number}"

class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return f"Copy {self.book_copy_id} of {self.book.title}"

class BookBorrow(models.Model):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return f"Borrow {self.borrow_id}"
