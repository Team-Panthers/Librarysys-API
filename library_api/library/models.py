from django.db import models
from django.contrib.auth import get_user_model

from library_api.fields import IncrementingField
from library_api.models import TimestampedModel


User = get_user_model()


class Library(TimestampedModel):
    no_of_racks = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Library-{self.pk}-{self.name}"


from book.models import BookCopy


class Rack(TimestampedModel):

    library = models.ForeignKey(Library, related_name="library_racks", on_delete=models.CASCADE)
    rack_no = IncrementingField(by_fields=['library'], editable=False, blank=True)
    book_copy = models.OneToOneField(BookCopy, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('library', 'rack_no')
        ordering = ['-rack_no', "-library"]

    def __str__(self):
        return f"Rack {self.rack_no} Library {self.library.name}"


