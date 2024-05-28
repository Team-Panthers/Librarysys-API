from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.db.models import Count

from .bookcopy_service import book_copy_service

from book.models import Book,Publisher,Author,BookCopy
from library.services.rack_service import rack_service
from user.services.user_service import user_service

from library_api.cache import CacheManager

book_cache = CacheManager(Book)

class BookService:

    def __init__(self,Book,Publisher,Author,rack_service,book_copy_service,user_service):
        self.Book = Book
        self.BookCopy = BookCopy
        self.Publisher = Publisher
        self.Author = Author
        self.rack_service = rack_service
        self.book_copy_service = book_copy_service
        self.user_service = user_service

    def all(self):
        books = book_cache.get_cache_data()
        if not books:
            books = self.Book.objects.all()
            book_cache.set_cache_data(books)
        return books

    @transaction.atomic
    def create_book(self, title, publishers, authors, library, number_of_copies):
        try:
            
            if not title or not library:
                raise ValueError("Title and library are required fields.")
            book_cache.clear_cache_data()
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
        
    def borrow_book(self,library,book,user,due_date):
        if self.user_service.can_user_borrow(user, library):
            if self.is_book_vaild(library,book):
                book_copy = self.rack_service.get_bookcopy_from_rack(library,book)
                if book_copy is not None:
                    borrow_book, error = self.book_copy_service.borrow_book_copy(library,user,book_copy,due_date)
                else:
                    borrow_book, error = self.book_copy_service.get_book_from_storage(library,book,user,due_date)
                if error is not None:
                    return None, error
                return borrow_book, None
            if isinstance(book,BookCopy):
                return None, "Invaild Book copy"
            return None, "Invalid book"
        else:
            if self.user_service.has_user_defaulted(user,library):
                return None, "User already exceeded the due date for a borrowed book and can't futher borrow until case resolved"

            if self.user_service.has_user_reached_limit(user,library):
                return None, "User already exceeded maximum limit for a borrowed book"
        return None, "An error occurred"




    def return_book(self, library, book_copy):
        rack, error = self.book_copy_service.return_book_copy(library, book_copy)
        if error:
            return None, error
        return rack, None

    def is_book_vaild(self,library,book):
        if isinstance(book,Book):
            return self.all().filter(library=library, id=book.id).exists()
        else:
            return self.all().filter(library=library, id=book.book.id).exists()

    def all_book_available(self,library):
        return self.all().filter(library=library)

    def book_available(self, library):
        # Annotate each book with the count of available copies
        qs = self.all_book_available(library).annotate(
            num_copies=Count('book_copies', filter=~Q(book_copies__is_borrowed=True))
        )

        # Filter out books with no available copies
        available_books = qs.filter(num_copies__gt=0)

        return available_books

    def search_books(self,queryset, query=None, publishers=None, authors=None,book_id=None):

        if query:
            queryset = queryset.filter(title__icontains=query)
            
        try:
            if book_id:
                if book_id.isdigit():
                    queryset = queryset.filter(book_id=int(book_id))
                else:
                    queryset = queryset.filter(book_id=book_id)
        except:
            queryset = queryset.none()

        if publishers:
            publisher_filters = Q()
            for publisher in publishers:
                publisher_filters |= Q(publisher__name__icontains=publisher)
            queryset = queryset.filter(publisher_filters)

        if authors:
            author_filters = Q()
            for author in authors:
                author_filters |= Q(authors__name__icontains=author)
            queryset = queryset.filter(author_filters)
        return queryset.distinct()


book_service = BookService(Book,Publisher,Author,rack_service,book_copy_service,user_service)