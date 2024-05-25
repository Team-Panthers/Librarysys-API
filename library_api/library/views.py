from book.serializers import BookSerializer, BorrowBookSerializer,BookCopySerializer

from library_api.mixins import UserContextMixin, LibraryAdminPermissionMixin,LibraryAdminCreateMixin,LibraryListMixin,LibraryRetrieveMixin,BookSearchMixin,LibraryContextMixin
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from .models import Rack
from .serializers import LibrarySerializer, LibraryBookAddSerializer, LibraryBorrowBookSerializer, \
    LibraryBorrowBookCopy, LibraryReturnSerializer, RackSerializer, StorageSerializer,UserSerializer
from .services.library_service import library_service
from book.services.book_service import book_service
from book.services.bookcopy_service import book_copy_service

from user.services.user_service import user_service


# Create your views here.

class LibraryListCreateView(UserContextMixin, generics.ListCreateAPIView):
    serializer_class = LibrarySerializer
    queryset = library_service.all()
    

class LibraryUpdateView(LibraryAdminPermissionMixin, UserContextMixin,generics.RetrieveUpdateAPIView):
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

class LibraryAvailableBookList(LibraryListMixin,BookSearchMixin):
    serializer_class = BookSerializer

    def get_queryset(self):
        library = self.library
        return book_service.book_available(library)

class LibraryAllBookList(LibraryListMixin,BookSearchMixin):
    serializer_class = BookSerializer

    def get_queryset(self):
        library = self.library
        qs = book_service.all_book_available(library)
        return qs


class LibraryAllBookCopies(LibraryListMixin):
    serializer_class = BookCopySerializer
    
    def get_queryset(self):
        library = self.library
        return book_copy_service.all_book_copy_available(library)
    
class LibraryAvailableBookCopies(LibraryListMixin):
    serializer_class = BookCopySerializer

    def get_queryset(self):
        library = self.library
        return book_copy_service.book_copy_available(library)

class LibraryBookGetBookCopies(LibraryRetrieveMixin):
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
    
class LibraryUsersList(LibraryAdminPermissionMixin,LibraryContextMixin,LibraryListMixin):
    serializer_class = UserSerializer

    def get_queryset(self):
        library = self.library
        return user_service.library_users(library)
    

class LibraryUserRetrieve(LibraryAdminPermissionMixin,LibraryContextMixin,generics.RetrieveAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        library = self.library
        return user_service.library_users(library)
    

    

        
        