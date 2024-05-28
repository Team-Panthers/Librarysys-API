from django.db import transaction

from library.models import Library, Rack
from book.models import Book,BookCopy

from library_api.cache import CacheManager


rack_cache = CacheManager(Rack)

class RackService:

    def __init__(self,Rack):
        self.Rack = Rack

    def all(self):
        racks = rack_cache.get_cache_data()
        if not racks:
            racks = self.Rack.objects.all()
            rack_cache.set_cache_data(racks)
        return racks

    @transaction.atomic
    def create_rack(self, library, no_of_racks):
        try:
            rack_cache.clear_cache_data()
            for _ in range(int(no_of_racks)):
                self.Rack.objects.create(library=library)
            return no_of_racks, None
        except Exception as e:
            return None, f"An error occurred: {e}"

    def get_available_racks_in_library(self,library):
        racks = self.all().filter(book_copy=None, library=library).order_by("rack_no")
        return racks

    def number_of_available_racks(self,library):
        return self.get_available_racks_in_library(library).count()

    def first_available_rack(self,library):
        return self.get_available_racks_in_library(library).first()

    def is_racks_available(self,library):
        return self.number_of_available_racks(library) > 0

    def add_bookcopy_to_rack(self,rack, bookcopy):
        rack_cache.clear_cache_data()
        rack.book_copy = bookcopy
        rack.save()
        return rack

    def remove_bookcopy_from_rack(self,rack):
        rack_cache.clear_cache_data()
        book_copy = rack.book_copy
        rack.book_copy = None
        rack.save()
        return book_copy


    def get_bookcopy_from_rack(self,library,book):
        if isinstance(book,Book):
            rack = self.all().filter(book_copy__book=book, library=library).first()
        else:
            rack = self.all().filter(book_copy=book, library=library).first()
            
        if rack:
            book_copy = rack.book_copy
            return book_copy
        return None






rack_service = RackService(Rack)