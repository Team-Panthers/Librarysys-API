from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from user.models import UserLibraryRelation
from library.models import Library


class IsLibraryAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            library_url_name = getattr(view, 'library_url_name', 'library_id')
            library_id = view.kwargs.get(library_url_name)

            if not library_id:
                raise PermissionDenied(detail="Library ID is required.")

            try:
                library = Library.objects.get(id=library_id)
                user_library_relation = UserLibraryRelation.objects.get(user=request.user, library=library)
                if not user_library_relation.is_admin:
                    raise PermissionDenied(detail="User is not an admin of this library.")
                return True
            except Library.DoesNotExist:
                raise PermissionDenied(detail="Library does not exist.")
            except UserLibraryRelation.DoesNotExist:
                raise PermissionDenied(detail="User is not an admin of this library.")
        raise PermissionDenied(detail="User is not authenticated.")


