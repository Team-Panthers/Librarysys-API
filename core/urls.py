from django.urls import path
from core.views import CreateLibrary, AddBookView, GetLibrary


urlpatterns = [

    path("library/", CreateLibrary.as_view(), name="library"),
    path("library/<int:pk>", GetLibrary.as_view(), name="library-detail"),
    path("library/<int:library_id>/add_book/", AddBookView.as_view(), name="add-book"),
]