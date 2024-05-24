from django.contrib.auth import get_user_model
from django.db import transaction

from book.models import Book,Publisher,Author,BookCopy,BookBorrow
from library.services.rack_service import rack_service
from library.models import Storage

class BookCopyService:

    def __init__(self,BookCopy,BookBorrow,Storage,rack_service):
        self.BookCopy = BookCopy
        self.BookBorrow = BookBorrow
        self.rack_service = rack_service
        self.Storage = Storage

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


    def borrow_book_copy(self,library,user,book_copy,due_date):
        borrow_book, error = self.mark_as_borrowed(library,user,book_copy,due_date)
        if error:
            return None, str(error)
        book_copy.is_borrowed = True
        if book_copy.rack:
            self.rack_service.remove_bookcopy_from_rack(book_copy.rack)
            book_copy.save()
        self.move_book_from_storage(library)
        return borrow_book,None

    def mark_as_borrowed(self,library,user,book_copy,due_date):
        try:
            book_borrowed = self.BookBorrow.objects.create(book_copy=book_copy,due_date=due_date,user=user, library=library)
            return book_borrowed,None
        except Exception as e:
            return None, e

    def return_book_copy(self, library, book_copy):
        try:
            book_borrow = self.BookBorrow.objects.get(book_copy=book_copy, library=library, is_returned=False)
            book_borrow.is_returned = True
            book_borrow.save()
            book_copy.is_borrowed = False
            book_copy.save()
            rack, error = self.add_bookcopy_to_rack(library,book_copy)
            if error:
                storage = self.Storage.objects.create(library=library, book_copy=book_copy)
                return storage, None
            return rack, None
        except BookBorrow.DoesNotExist:
            return None, "This book copy is not borrowed"

    def move_book_from_storage(self,library):
        storage = self.Storage.objects.filter(library=library).first()
        if storage:
            rack, error = self.add_bookcopy_to_rack(library,storage.book_copy)
            if error is None:
                storage.delete()
            return rack, error
        return None, "No book copy in Storage"

    def get_book_from_storage(self,library,book,user,due_date):
        if isinstance(book,Book):
            storage = self.Storage.objects.filter(library=library,book_copy__book=book).first()
        else:
            storage = self.Storage.objects.filter(library=library,book_copy=book).first()
        if storage:
            book_copy = storage.book_copy
            storage.delete()
            borrow_book, error = self.borrow_book_copy(library,user,book_copy,due_date)
            if error:
                self.Storage.objects.create(library=library, book_copy=book_copy)
                return None,error
            return borrow_book, None
        return None,"Book copied already Borrowed"


    def add_bookcopy_to_rack(self,library,book_copy):
        if self.rack_service.is_racks_available(library):
            rack = self.rack_service.first_available_rack(library)
            rack = self.rack_service.add_bookcopy_to_rack(rack, book_copy)
            return rack, None
        return None,"No available Rack"

    def all_book_copy_available(self, library):
        return self.all().filter(library=library)

    def book_copy_available(self, library):
        # Filter out book copies that are not borrowed
        available_book_copies = self.all_book_copy_available(library).filter(is_borrowed=False)

        return available_book_copies

    def all_copies_for_book(self, library, book):
        return self.all().filter(library=library, book=book)





book_copy_service = BookCopyService(BookCopy,BookBorrow,Storage,rack_service)