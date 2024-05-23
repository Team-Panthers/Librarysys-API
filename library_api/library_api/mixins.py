from .permissions import IsLibraryAdmin
from rest_framework.permissions import IsAuthenticated

class UserContextMixin():

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class LibraryAdminPermissionMixin():
    permission_classes = [IsAuthenticated, IsLibraryAdmin]