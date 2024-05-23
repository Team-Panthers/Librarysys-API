from django.contrib.auth import get_user_model
from django.db import transaction

from library.models import Library, Rack
from user.models import UserLibraryRelation

User = get_user_model()


class LibraryService:
    
    @transaction.atomic
    def create_library(self, name, no_of_racks,admin_user):
        try:
            library = Library.objects.create(name=name,no_of_racks=no_of_racks)
            
            self.create_rack(library, no_of_racks)
            
            UserLibraryRelation.objects.create(user=admin_user,library=library, is_admin=True)
            
            return library,None
        except Exception as e:
            return None, f"An error occurred: {e}"
        
    @staticmethod
    @transaction.atomic  
    def create_rack(library,no_of_racks):
       try:
            for _ in range(int(no_of_racks)):
                Rack.objects.create(library=library)
                return no_of_racks,None
       except Exception as e:
           return None, f"An error occurred: {e}"
       
    
    def edit_library(self,library,**kwargs):
        try:
            no_of_racks = kwargs.get('no_of_racks')
            name = kwargs.get("name")
            
            if no_of_racks is not None:
                self.create_rack(library=library,no_of_racks=int(no_of_racks))
                library.no_of_racks = library.no_of_racks + no_of_racks
                
            if name is not None:
                library.name = name
            
            library.save()
            return library, None
        except Exception as e:
            return None, f"An error occurred: {e}"
        
    
    
            
        
        