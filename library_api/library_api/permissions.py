from rest_framework.permissions import BasePermission
from rest_framework import permissions
from user.models import UserLibraryRelation


class IsLibraryAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin for the library related to the object being accessed
        if request.user:
            try:
                # Check if the user is an admin for the library
                user_library_relation = UserLibraryRelation.objects.get(user=request.user, library=obj)
                return user_library_relation.is_admin
            except UserLibraryRelation.DoesNotExist:
                return False
        return False
