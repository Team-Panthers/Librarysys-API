from django.db import transaction

from library.models import Library, Rack


class RackService:

    def __init__(self,Rack):
        self.Rack = Rack

    def all(self):
        return self.Rack.objects.all()

    @transaction.atomic
    def create_rack(self, library, no_of_racks):
        try:
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
        rack.book_copy = bookcopy
        rack.save()




rack_service = RackService(Rack)