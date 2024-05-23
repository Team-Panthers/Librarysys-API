from django.contrib.auth import get_user_model
from django.db import transaction

from user.models import UserLibraryRelation

User = get_user_model()


class UserService:

    @staticmethod
    def create_user(email, password):
        try:
            user = User.objects.create_user(email, password)
            return user, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_user_libraries(user):
        return UserLibraryRelation.objects.filter(user=user)

    def can_user_borrow(self, user, library):
        return not (self.has_user_defaulted(user) and self.has_user_reached_limit(user, library))

    def get_user_borrowed_books(self, user, library):
        borrowed_books = self.get_all_user_borrowed_books(user).filter(library=library)
        return borrowed_books

    @staticmethod
    def get_all_user_borrowed_books(user):
        borrowed_books = user.books_borrowed.filter(is_returned=False)
        return borrowed_books

    def user_defaulted_books(self, user):
        borrowed_books = self.get_all_user_borrowed_books(user)
        defaulted_books = [book_borrow for book_borrow in borrowed_books if book_borrow.is_overdue]
        return defaulted_books

    def has_user_defaulted(self, user):
        return len(self.user_defaulted_books(user)) > 0

    def has_user_reached_limit(self, user, library):
        user_relation = self.get_user_libraries(user).filter(library=library)
        total_borrowed = self.get_user_borrowed_books(user, library).count()
        if user_relation.exists():
            if user_relation.is_admin:
                return False
            return total_borrowed >= user_relation.first().max_num_books
        else:
            _, error = self.add_user_to_library(library, user, is_admin=False)
            if error:
                return True
            return False

    @staticmethod
    def add_user_to_library(library, user, is_admin=False):
        try:
            return UserLibraryRelation.objects.create(user=user, library=library, is_admin=is_admin), None
        except Exception as e:
            return None, f"An error occurred: {e}"

    @staticmethod
    def is_user_library_admin(user, library):
        return user.is_library_admin(library)


user_service = UserService()
