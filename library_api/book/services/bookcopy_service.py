from django.contrib.auth import get_user_model
from django.db import transaction

from book.models import Book,Publisher,Author,BookCopy
from library.services.rack_service import rack_service

class BookCopyService:

    def __init__(self,BookCopy,rack_service):
        self.BookCopy = BookCopy
        self.rack_service = rack_service

    def all(self):
        return self.BookCopy.objects.all()

    def create_book_copy(self,book):
        try:
            rack = self.rack_service.first_available_rack(book.library)
            book_copy = self.BookCopy.objects.create(book=book, library=book.library)
            self.rack_service.add_bookcopy_to_rack(rack, book_copy)
            return book_copy, None
        except Exception as e:
            return None, str(e)

book_copy_service = BookCopyService(BookCopy,rack_service)