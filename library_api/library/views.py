from book.serializers import BookSerializer, BorrowBookSerializer,BookCopySerializer

from library_api.mixins import UserContextMixin, LibraryAdminPermissionMixin,LibraryAdminCreateMixin,LibraryListMixin,LibraryRetrieveMixin
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Rack
from .serializers import LibrarySerializer, LibraryBookAddSerializer, LibraryBorrowBookSerializer, \
    LibraryBorrowBookCopy, LibraryReturnSerializer, RackSerializer, StorageSerializer
from .services.library_service import library_service
from book.services.book_service import book_service
from book.services.bookcopy_service import book_copy_service


# Create your views here.

class LibraryListCreateView(UserContextMixin, generics.ListCreateAPIView):
    serializer_class = LibrarySerializer
    queryset = library_service.all()
    


class LibraryUpdateView(UserContextMixin,LibraryAdminPermissionMixin, generics.RetrieveUpdateAPIView):
    library_url_name = "pk"
    serializer_class = LibrarySerializer
    queryset = library_service.all()
    http_method_names = ['get', 'patch']


class LibraryAddBookApiView(LibraryAdminCreateMixin):
    serializer_class = LibraryBookAddSerializer
    response_serializer_class = BookSerializer


class LibraryBorrowBookApiView(LibraryAdminCreateMixin):
    serializer_class = LibraryBorrowBookSerializer
    response_serializer_class = BorrowBookSerializer


class LibraryBorrowBookCopyApiView(LibraryAdminCreateMixin):
    serializer_class = LibraryBorrowBookCopy
    response_serializer_class = BorrowBookSerializer


class LibraryReturnBookCopyApiView(LibraryAdminCreateMixin):
    serializer_class = LibraryReturnSerializer

    def get_response_serializer(self, instance):
        if isinstance(instance, Rack):
            return RackSerializer(instance)
        return StorageSerializer(instance)

class LibraryAvailableBookList(LibraryListMixin):
    serializer_class = BookSerializer

    def get_queryset(self):
        library = self.get_library()
        return book_service.book_available(library)

class LibraryAllBookList(LibraryListMixin):
    serializer_class = BookSerializer

    def get_queryset(self):
        library = self.get_library()
        return book_service.all_book_available(library)


class LibraryAllBookCopies(LibraryListMixin):
    serializer_class = BookCopySerializer
    def get_queryset(self):
        library = self.get_library()
        return book_copy_service.all_book_copy_available(library)
    
class LibraryAvailableBookCopies(LibraryListMixin):
    serializer_class = BookCopySerializer

    def get_queryset(self):
        library = self.get_library()
        return book_copy_service.book_copy_available(library)

class LibraryBookGetBookCopies(LibraryRetrieveMixin):
    def retrieve(self, request, *args, **kwargs):
        library = self.get_library()
        book = self.get_object()

        if not book_service.is_book_vaild(library,book):
            raise NotFound("Book is not available in this library")
        book_copies = book_copy_service.all_copies_for_book(library,book)
        serializer = BookCopySerializer(book_copies, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        library = self.get_library()
        return book_service.all_book_available(library)

