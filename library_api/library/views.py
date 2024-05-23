from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import LibrarySerializer,LibraryBookAddSerializer
from .services.library_service import library_service
from book.serializers import BookSerializer

from library_api.mixins import UserContextMixin,LibraryAdminPermissionMixin


# Create your views here.

class LibraryListCreateView(UserContextMixin, generics.ListCreateAPIView):
    serializer_class = LibrarySerializer
    queryset = library_service.all()


class LibraryUpdateView(UserContextMixin,LibraryAdminPermissionMixin, generics.RetrieveUpdateAPIView):
    serializer_class = LibrarySerializer
    queryset = library_service.all()
    http_method_names = ['get', 'patch']


class LibraryAddBookApiView(LibraryAdminPermissionMixin, generics.CreateAPIView):
    serializer_class = LibraryBookAddSerializer

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

