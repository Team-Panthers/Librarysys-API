from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from user.models import UserLibraryRelation
from library.models import Library


class IsLibraryAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user:
            library_id = request.data.get('library')
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
                raise PermissionDenied(detail="User does not have a relation with this library.")
        raise PermissionDenied(detail="User is not authenticated.")

    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin for the library related to the object being accessed
        if request.user:
            try:
                # Check if the user is an admin for the library
                user_library_relation = UserLibraryRelation.objects.get(user=request.user, library=obj)
                if not user_library_relation.is_admin:
                    raise PermissionDenied(detail="User is not an admin of this library.")
                return True
            except UserLibraryRelation.DoesNotExist:
                raise PermissionDenied(detail="User does not have a relation with this library.")
        raise PermissionDenied(detail="User is not authenticated.")
