from django.contrib.auth import get_user_model
from django.db import transaction

from .bookcopy_service import book_copy_service

from book.models import Book,Publisher,Author,BookCopy
from library.services.rack_service import rack_service

class BookService:

    def __init__(self,Book,Publisher,Author,rack_service,book_copy_service):
        self.Book = Book
        self.BookCopy = BookCopy
        self.Publisher = Publisher
        self.Author = Author
        self.rack_service = rack_service
        self.book_copy_service = book_copy_service

    def all(self):
        return self.Book.objects.all()

    @transaction.atomic
    def create_book(self, title, publishers, authors, library, number_of_copies):
        try:
            if not title or not library:
                raise ValueError("Title and library are required fields.")

            if self.is_rackspace_enough(library, number_of_copies):
                # Create the book
                book = self.Book.objects.create(title=title, library=library)

                # Add publishers to the book
                self.create_publisher(book, publishers)

                # Add authors to the book
                self.create_author(book, authors)

                # create the book copies
                for copy in range(number_of_copies):
                    book_copy, error = self.book_copy_service.create_book_copy(book)
                    if error:
                        raise Exception(error)

                return book, None
            else:
                return None, f"the number of rack availability is {self.rack_service.number_of_available_racks(library)} and the book copy exceeds it"
        except Exception as e:
            return None, f"An error occurred: {e}"

    def is_rackspace_enough(self,library,bookcopies):
        space = self.rack_service.number_of_available_racks(library)
        return space >= bookcopies

    @transaction.atomic
    def create_publisher(self,book,publishers):
        for publisher_name in publishers:
            publisher, created = self.Publisher.objects.get_or_create(
                name__iexact=publisher_name, library=book.library,
                defaults={'name': publisher_name, 'library': book.library}
            )
            book.publisher.add(publisher)

        book.save()

    @transaction.atomic
    def create_author(self,book,authors):
        for author_name in authors:
            author, created = self.Author.objects.get_or_create(
                name__iexact=author_name, library=book.library,
                defaults={'name': author_name, 'library': book.library}
            )
            book.authors.add(author)

        book.save()


book_service = BookService(Book,Publisher,Author,rack_service,book_copy_service)