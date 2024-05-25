from django.contrib.auth import get_user_model
from django.db import transaction

from user.models import UserLibraryRelation

from book.models import BookBorrow



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
        return not (self.has_user_defaulted(user,library) or self.has_user_reached_limit(user, library))

    def get_user_borrowed_books(self, user, library):
        borrowed_books = BookBorrow.objects.filter(user=user,library=library,is_returned=False)
        return borrowed_books

    @staticmethod
    def get_all_user_borrowed_books(user):
        borrowed_books = BookBorrow.objects.filter(user=user,is_returned=False)
        return borrowed_books

    def user_defaulted_books(self, user):
        borrowed_books = self.get_all_user_borrowed_books(user)
        defaulted_books = [book_borrow for book_borrow in borrowed_books if book_borrow.is_overdue]
        return defaulted_books

    def has_user_defaulted(self, user,library):
        if self.is_user_library_admin(user,library):
            return False

        return len(self.user_defaulted_books(user)) > 0

    def has_user_reached_limit(self, user, library):
        user_relation = self.get_user_libraries(user).filter(library=library)
        total_borrowed = self.get_user_borrowed_books(user, library).count()
        if user_relation.exists():
            user_relation = user_relation.first()
            if user_relation.is_admin:
                return False
            return total_borrowed >= user_relation.max_num_books
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

    def library_users(self,library):
        user_relations = UserLibraryRelation.objects.filter(library=library, is_admin=False)
        users = self.all().filter(id__in=user_relations.values('user_id'))
        return users
        
    def all(self):
        return User.objects.all()

user_service = UserService()
