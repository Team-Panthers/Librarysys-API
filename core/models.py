from django.db import models
from django.contrib.auth.models import User


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Library(TimeStamp):
    name = models.CharField(max_length=100)
    no_of_rack = models.PositiveIntegerField()

    def __str__(self):
        return f"Library {self.name}"


class Publisher(TimeStamp):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(TimeStamp):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(TimeStamp):
    title = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class Rack(TimeStamp):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='racks')
    book_copy = models.OneToOneField('BookCopy', on_delete=models.CASCADE, null=True, blank=True, related_name='rack')
    rack_number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Rack {self.rack_number} of Library {self.library.name}"


class BookCopy(TimeStamp):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    is_borrowed = models.BooleanField(default=False)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='book_copies')

    def __str__(self):
        return f"Copy {self.id} of {self.book.title} in {self.library.name}"


class BookBorrow(TimeStamp):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='borrows')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_borrows')
    borrow_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return f"Borrow {self.id} by {self.user.username}"
