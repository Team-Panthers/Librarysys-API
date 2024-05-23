from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from library.models import Library

from library_api.models import TimestampedModel
from library_api.fields import IncrementingField

User = get_user_model()


class Publisher(TimestampedModel):
    name = models.CharField(max_length=255)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='publishers')

    def __str__(self):
        return f"{self.name}-{self.library.name}"


class Author(TimestampedModel):
    name = models.CharField(max_length=255)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='authors')

    def __str__(self):
        return f"{self.name}-{self.library.name}"


class Book(TimestampedModel):
    title = models.CharField(max_length=255)
    publisher = models.ManyToManyField(Publisher)
    authors = models.ManyToManyField(Author)
    book_id = IncrementingField(by_fields=['library'], editable=False, blank=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title}-{self.library.name}"

    class Meta:
        unique_together = ('library', 'book_id')


class BookCopy(TimestampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_borrowed = models.BooleanField(default=False)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='book_copies')
    book_copy_id = IncrementingField(by_fields=['library', "book"], editable=False, blank=True)

    def __str__(self):
        return f"Copy {self.book_copy_id} of {self.book}"

    class Meta:
        unique_together = ('library', 'book', "book_copy_id")


class BookBorrow(TimestampedModel):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_borrowed')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='books_borrowed')
    due_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    @property
    def is_overdue(self):
        if self.is_returned:
            return False
        if self.due_date < timezone.now().date():
            return False
        return True

    def __str__(self):
        return f"Borrow {self.book_copy}"
