from .permissions import IsLibraryAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.exceptions import NotFound

from rest_framework import status
from rest_framework.response import Response

from library.models import Library
from library.services.library_service import library_service
class UserContextMixin():

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class LibraryContextMixin():
    library_url_name = "library_id"
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['library'] = Library.objects.get(id=self.kwargs[self.library_url_name])
        return context


class CreateResponseMixin:
    response_serializer_class = None
    def get_queryset(self):
        return []

    def get_response_serializer(self, instance):
        if self.response_serializer_class is None:
            raise ValueError("response_serializer_class must be set")
        return self.response_serializer_class(instance)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_data = self.get_response_serializer(instance).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibraryAdminPermissionMixin():
    permission_classes = [IsAuthenticated, IsLibraryAdmin]

class LibraryAdminCreateMixin(LibraryAdminPermissionMixin, LibraryContextMixin, CreateResponseMixin,
                               generics.CreateAPIView):
    pass

class GetLibraryMixin:
    def get_library(self):
        library_id = self.kwargs.get('library_id')
        try:
            return library_service.all().get(id=library_id)
        except library_service.Library.DoesNotExist:
            raise NotFound("Library does not exist")

class LibraryListMixin(GetLibraryMixin,generics.ListAPIView):
    pass


class LibraryRetrieveMixin(GetLibraryMixin,generics.RetrieveAPIView):
    pass

