from book.serializers import BookSerializer, BorrowBookSerializer,BookCopySerializer,BookCopyDetailSerializer

from library_api.mixins import UserContextMixin, LibraryAdminPermissionMixin,LibraryAdminCreateView,LibraryListView,LibraryRetrieveView,BookSearchMixin,LibraryContextMixin,BookCopySearchMixin
from rest_framework import generics

from .models import Rack
from .serializers import LibrarySerializer, LibraryBookAddSerializer, LibraryBorrowBookSerializer, \
    LibraryBorrowBookCopy, LibraryReturnSerializer, RackSerializer, StorageSerializer,UserSerializer
from .services.library_service import library_service
from book.services.book_service import book_service
from book.services.bookcopy_service import book_copy_service

from user.services.user_service import user_service
from book.services.book_service import book_cache


# Create your views here.

class LibraryListCreateView(UserContextMixin, generics.ListCreateAPIView):
    serializer_class = LibrarySerializer
    queryset = library_service.all()
    

class LibraryUpdateView(LibraryAdminPermissionMixin, UserContextMixin,generics.RetrieveUpdateAPIView):
    serializer_class = LibrarySerializer
    queryset = library_service.all()
    http_method_names = ['get', 'patch']


class LibraryAddBookApiView(LibraryAdminCreateView):
    serializer_class = LibraryBookAddSerializer
    response_serializer_class = BookSerializer


class LibraryBorrowBookApiView(LibraryAdminCreateView):
    serializer_class = LibraryBorrowBookSerializer
    response_serializer_class = BorrowBookSerializer


class LibraryBorrowBookCopyApiView(LibraryAdminCreateView):
    serializer_class = LibraryBorrowBookCopy
    response_serializer_class = BorrowBookSerializer


class LibraryReturnBookCopyApiView(LibraryAdminCreateView):
    serializer_class = LibraryReturnSerializer

    def get_response_serializer(self, instance):
        if isinstance(instance, Rack):
            return RackSerializer(instance)
        return StorageSerializer(instance)

class LibraryUsersList(LibraryAdminPermissionMixin,LibraryContextMixin,LibraryListView):
    serializer_class = UserSerializer

    def get_queryset(self):
        library = self.library
        return user_service.library_users(library)
    

class LibraryUserRetrieve(LibraryAdminPermissionMixin,LibraryContextMixin,generics.RetrieveAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        library = self.library
        return user_service.library_users(library)
    

class LibraryAdminRetrieveDeleteBook(LibraryAdminPermissionMixin,generics.RetrieveDestroyAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        library = self.library
        qs = book_service.all_book_available(library)
        return qs

class LibraryAdminRetrieveDeleteBookCopy(LibraryAdminPermissionMixin,generics.RetrieveDestroyAPIView):
    serializer_class = BookCopyDetailSerializer
    
    def get_queryset(self):
        library = self.library
        qs = book_copy_service.all_book_copy_available(library)
        return qs
    
    
    def perform_destroy(self, instance):
        book_cache.clear_cache_data()
        book_cache.clear_cache_data(instance.id)
        return super().perform_destroy(instance)
    
    
        
        