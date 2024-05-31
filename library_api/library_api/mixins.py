from book.services.book_service import book_service
from book.services.bookcopy_service import book_copy_service
from library.models import Library
from library.services.library_service import library_service
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.core.exceptions import FieldDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsLibraryAdmin


class ConfirmLibraryDispatchMixin():
    library_lookup_field = "pk"
    library_lookup_url_kwarg = "library_id"
    _library = None
    library_error_msg = 'Library not found'
    
    
    def dispatch(self, request, *args, **kwargs):
        if not(self.library_lookup_field or self.library_lookup_url_kwarg):
            raise ValueError('library_lookup_field or library_lookup_url_kwarg must be set')
        if self.library_lookup_field == None:
            raise ValueError("library_lookup_field must be set")
        lookup_value = kwargs.get(self.library_lookup_url_kwarg) or kwargs.get(self.library_lookup_field)
        
        if lookup_value is None:
            raise ValueError(f"URL kwarg '{self.library_lookup_field}' must be provided")
        
        try:
            if not self.library_lookup_field == "pk":
                Library._meta.get_field(self.library_lookup_field)
        except FieldDoesNotExist:
            raise ValueError(f"Field '{self.library_lookup_field}' does not exist on Library model")
        try:
            library = library_service.all().get(**{self.library_lookup_field: lookup_value})
            self._library = library
        except library_service.Library.DoesNotExist:
            self.library_error_msg = 'Library does not exist'
            self._library = None
        except library_service.Library.MultipleObjectsReturned:
            self.library_error_msg = "Multiple libraries found for the given criteria"
            self._library = None
        
        return super().dispatch(request, *args, **kwargs)
    
    @property
    def library(self):
        if self._library is None:
            raise NotFound(self.library_error_msg)
        return self._library
    


class UserContextMixin:

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class LibraryContextMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.library is None:
            raise ValueError("library instance was not provided")
        context['library'] = self.library
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


class RetrieveResponseMixin:
    obj_error_message = "Object does not exist"
    object_queryset = None

    def get_object_queryset(self):
        qs = None
        if self.object_queryset is not None:
            qs = self.object_queryset
        return qs

    def get_object(self):
        try:
            lookup_value = self.kwargs.get(self.lookup_url_kwarg or self.lookup_field)
            qs = self.get_object_queryset()
            object_model = qs.model
            if qs == None:
                raise ValueError("object_queryset must be set")
            filter_kwargs = {self.lookup_field: lookup_value}
            obj = qs.get(**filter_kwargs)

            if obj is None:
                raise NotFound(self.obj_error_message)
        
        except object_model.DoesNotExist:
            raise NotFound(self.obj_error_message)
        except object_model.MultipleObjectsReturned:
            raise ValueError("Mutiple Object was return to returned")

        return obj

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookSearchMixin:

    def filter_queryset(self, queryset):
        query = self.request.GET.get('title', "")
        book_id = self.request.GET.get('book_id', "")
        authors_str = self.request.GET.get('authors', "")
        publishers_str = self.request.GET.get('publishers', "")

        authors = authors_str.split(',') if authors_str else []
        publishers = publishers_str.split(',') if publishers_str else []

        queryset = book_service.search_books(queryset, query, publishers, authors,book_id)

        return super().filter_queryset(queryset)
    
class BookCopySearchMixin:
    
    def filter_queryset(self, queryset):
        query = self.request.GET.get('title', "")
        book_id = self.request.GET.get('book_id', "")
        book_copy_id = self.request.GET.get('book_copy_id', "")
        authors_str = self.request.GET.get('authors', "")
        publishers_str = self.request.GET.get('publishers', "")

        authors = authors_str.split(',') if authors_str else []
        publishers = publishers_str.split(',') if publishers_str else []

        queryset = book_copy_service.search_book_copies(queryset, query, publishers, authors,book_copy_id,book_id)

        return super().filter_queryset(queryset)


class LibraryAdminPermissionMixin(ConfirmLibraryDispatchMixin):
    permission_classes = [IsAuthenticated, IsLibraryAdmin]


class LibraryAdminCreateView(LibraryAdminPermissionMixin, LibraryContextMixin, CreateResponseMixin,
                              generics.CreateAPIView):
    pass

class LibraryListView(ConfirmLibraryDispatchMixin,generics.ListAPIView):
    pass


class LibraryRetrieveView(ConfirmLibraryDispatchMixin, RetrieveResponseMixin, generics.RetrieveAPIView):
    pass

