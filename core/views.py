from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView
from core.models import Library
from core.serializers import AddBookSerializer, LibrarySerializer

class CreateLibrary(ListCreateAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class GetLibrary(RetrieveAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def get(self, request, *args, **kwargs):
        print(kwargs)
        return self.retrieve(request, *args, **kwargs)

class AddBookView(CreateAPIView):
    serializer_class = AddBookSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['library_id'] = self.kwargs.get('library_id')
        return context





