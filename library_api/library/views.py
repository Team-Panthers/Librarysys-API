from book.serializers import BookSerializer, BorrowBookSerializer
from library_api.mixins import UserContextMixin, LibraryAdminPermissionMixin,LibraryAdminCreateMixin
from rest_framework import generics

from .models import Rack
from .serializers import LibrarySerializer, LibraryBookAddSerializer, LibraryBorrowBookSerializer, \
    LibraryBorrowBookCopy, LibraryReturnSerializer, RackSerializer, StorageSerializer
from .services.library_service import library_service


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
