from django.contrib import admin

from .models import Rack,Library

# Register your models here.

admin.site.register(Library)

class RackAdmin(admin.ModelAdmin):
    list_display = ('library', 'rack_no')  # Display the fields in the list view
    readonly_fields = ('rack_no',)  # Make rack_no readonly in the detail view

admin.site.register(Rack, RackAdmin)