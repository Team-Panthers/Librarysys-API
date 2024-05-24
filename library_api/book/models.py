from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

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



    class Meta:
        unique_together = ('library', 'book_id')


class BookCopy(TimestampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='book_copies')
    is_borrowed = models.BooleanField(default=False)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='book_copies')
    order = IncrementingField(by_fields=['library', "book"], editable=False, blank=True)
    book_copy_id = IncrementingField(by_fields=['library'], editable=False, blank=True)

    def __str__(self):
        return f"Copy {self.order} of {self.book}"

    class Meta:
        unique_together = ('library', 'book', "order")


class BookBorrow(TimestampedModel):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_borrowed')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='books_borrowed')
    due_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and self.due_date <= timezone.now().date():
            raise ValidationError("The due date must be a date in the future.")
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.is_returned:
            return False
        if self.due_date < timezone.now().date():
            return True
        return False

    def __str__(self):
        return f"Borrow {self.book_copy}"
