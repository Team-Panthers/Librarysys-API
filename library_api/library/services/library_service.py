from book.services.book_service import book_service
from django.db import transaction
from library.models import Library, Rack
from user.models import UserLibraryRelation

from .rack_service import rack_service

from library_api.cache import CacheManager

library_cache = CacheManager(Library)

class LibraryService:

    def __init__(self, Library, Rack, UserLibraryRelation, rack_service, book_service):
        self.Library = Library
        self.Rack = Rack
        self.UserLibraryRelation = UserLibraryRelation
        self.rack_service = rack_service
        self.book_service = book_service

    @transaction.atomic
    def create_library(self, name, no_of_racks, admin_user):
        try:
            library = self.Library.objects.create(name=name, no_of_racks=no_of_racks)

            self.rack_service.create_rack(library, no_of_racks)

            self.UserLibraryRelation.objects.create(user=admin_user, library=library, is_admin=True)
            library_cache.clear_cache_data()
            library_cache.set_cache_data(library,library.id)
            return library, None
        except Exception as e:
            return None, f"An error occurred: {e}"

    def edit_library(self, library, **kwargs):
        try:
            no_of_racks = kwargs.get('no_of_racks')
            name = kwargs.get("name")

            if no_of_racks is not None:
                self.rack_service.create_rack(library=library, no_of_racks=int(no_of_racks))
                library.no_of_racks = library.no_of_racks + no_of_racks

            if name is not None:
                library.name = name

            library.save()
            library_cache.clear_cache_data()
            library_cache.set_cache_data(library,library.id)
            return library, None
        except Exception as e:
            return None, f"An error occurred: {e}"

    def all(self):
        libraries = library_cache.get_cache_data()
        if not libraries:
            libraries = self.Library.objects.all()
            library_cache.set_cache_data(libraries)
        return libraries

    def get(self, library_id):
        try:
            library = library_cache.get_cache_data(library_id)
            if not library:
                library = self.all().get(id=library_id)
                library_cache.set_cache_data(library,library_id)
            return library
        except Exception:
            return None

    def add_book(self, **kwargs):
        try:
            book, error = self.book_service.create_book(**kwargs)
            if error:
                return None, error
            return book, None
        except Exception as e:
            return None, str(e)

    def borrow_book(self, library, book, user, due_date):
        try:
            borrow_book, error = self.book_service.borrow_book(library, book, user, due_date)
            if error:
                return None, error
            return borrow_book, error
        except Exception as e:
            print(e)
            return None, e


    def return_book(self, library, book_copy):
        try:
            rack, error = self.book_service.return_book(library, book_copy)
            return rack, error
        except Exception as e:
            return None, str(e)


library_service = LibraryService(Library, Rack, UserLibraryRelation, rack_service, book_service)
