from django.db import models
from django.contrib.auth import get_user_model

from library_api.fields import IncrementingField
from library_api.models import TimestampedModel




class Library(TimestampedModel):
    no_of_racks = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pk}-{self.name}"

    class Meta:
        verbose_name_plural = "libraries"


from book.models import BookCopy


class Rack(TimestampedModel):

    library = models.ForeignKey(Library, related_name="library_racks", on_delete=models.CASCADE)
    rack_no = IncrementingField(by_fields=['library'], editable=False, blank=True)
    book_copy = models.OneToOneField(BookCopy, on_delete=models.SET_NULL, null=True, blank=True, related_name='rack')

    class Meta:
        unique_together = ('library', 'rack_no')
        ordering = ['-rack_no', "-library"]

    def __str__(self):
        return f"Rack {self.rack_no} {self.library.name}"


class Storage(TimestampedModel):

    library = models.ForeignKey(Library, related_name="storage", on_delete=models.CASCADE)
    storage_no = IncrementingField(by_fields=['library'], editable=False, blank=True)
    book_copy = models.OneToOneField(BookCopy, on_delete=models.SET_NULL, null=True, blank=True, related_name='storage')

    class Meta:
        unique_together = ('library', 'storage_no')
        ordering = ['-storage_no', "-library"]

    def __str__(self):
        return f"Rack {self.storage_no} {self.library.name}"