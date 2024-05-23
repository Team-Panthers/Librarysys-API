from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import LibrarySerializer

from .services.library_service import library_service
from library_api.permissions import IsLibraryAdmin
from library_api.mixins import UserContextMixin


# Create your views here.

class LibraryListCreateView(UserContextMixin, generics.ListCreateAPIView):
    serializer_class = LibrarySerializer
    queryset = library_service.all()


class LibraryUpdateView(UserContextMixin, generics.RetrieveUpdateAPIView):
    serializer_class = LibrarySerializer
    queryset = library_service.all()
    permission_classes = [IsAuthenticated, IsLibraryAdmin]
    http_method_names = ['get', 'patch']
