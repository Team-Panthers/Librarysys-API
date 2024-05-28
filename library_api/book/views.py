from book.serializers import BookSerializer,BookCopySerializer
from library_api.mixins import BookSearchMixin,BookCopySearchMixin,LibraryListView, LibraryRetrieveView
from book.services.book_service import book_service
from book.services.bookcopy_service import book_copy_service


class LibraryAvailableBookList(BookSearchMixin,LibraryListView):
    serializer_class = BookSerializer

    def get_queryset(self):
        library = self.library
        return book_service.book_available(library)

class LibraryAllBookList(BookSearchMixin,LibraryListView):
    serializer_class = BookSerializer

    def get_queryset(self):
        library = self.library
        qs = book_service.all_book_available(library)
        return qs


class LibraryAllBookCopies(BookCopySearchMixin,LibraryListView):
    serializer_class = BookCopySerializer
    
    def get_queryset(self):
        library = self.library
        return book_copy_service.all_book_copy_available(library)
    
class LibraryAvailableBookCopies(BookCopySearchMixin,LibraryListView):
    serializer_class = BookCopySerializer

    def get_queryset(self):
        library = self.library
        return book_copy_service.book_copy_available(library)

class LibraryBookGetBookCopies(LibraryRetrieveView):
    serializer_class = BookCopySerializer
    obj_error_message = "Book Not Found in the Library"

    
    def get_object_queryset(self):
        library = self.library
        qs = book_service.all_book_available(library)
        return qs

    def get_queryset(self):
        library = self.library
        book = self.get_object()
        return book_copy_service.all_copies_for_book(library,book)