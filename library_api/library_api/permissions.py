from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from user.models import UserLibraryRelation
from library.models import Library


class IsLibraryAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            try:
                library = view.library
                if library is None:
                    raise("Library Cannot be Null")
                user_library_relation = UserLibraryRelation.objects.get(user=request.user, library=library)
                if not user_library_relation.is_admin:
                    raise PermissionDenied(detail="User is not an admin of this library.")
                return True
            except UserLibraryRelation.DoesNotExist:
                UserLibraryRelation.objects.create(user=request.user,library=library)
                raise PermissionDenied(detail="User is not an admin of this library.")
        raise PermissionDenied(detail="User is not authenticated.")


