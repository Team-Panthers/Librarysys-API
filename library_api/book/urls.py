from django.urls import path
from .views import *

urlpatterns = [
    path("available/<int:library_id>/", LibraryAvailableBookList.as_view(), name="library_book_list"),
    path("all/<int:library_id>/", LibraryAllBookList.as_view(), name="library_all_book_list_and_search"),
    path("copies/<int:library_id>/<int:pk>/", LibraryBookGetBookCopies.as_view(), name="library_get_bookcopies_for_book"),
    
    path("available-copies/<int:library_id>/", LibraryAvailableBookCopies.as_view(), name="library_available_book_copies"),
    path("all-copies/<int:library_id>/", LibraryAllBookCopies.as_view(), name="library_all_book_copies"),
]
