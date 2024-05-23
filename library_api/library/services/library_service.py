from django.db import transaction
from library.models import Library, Rack
from user.models import UserLibraryRelation

from .rack_service import rack_service
from book.services.book_service import book_service



class LibraryService:

    def __init__(self, Library, Rack, UserLibraryRelation, rack_service,book_service):
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
            return library, None
        except Exception as e:
            return None, f"An error occurred: {e}"

    def all(self):
        libraries = self.Library.objects.all()
        return libraries

    def add_book(self, **kwargs):
        try:
            book, error = self.book_service.create_book(**kwargs)
            if error:
                return None, error
            return book,None
        except Exception as e:
            return None, str(e)


library_service = LibraryService(Library, Rack, UserLibraryRelation, rack_service, book_service)
