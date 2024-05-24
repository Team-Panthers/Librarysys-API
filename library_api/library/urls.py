from django.urls import path

from .views import LibraryListCreateView,LibraryUpdateView,LibraryAddBookApiView,LibraryBorrowBookApiView,LibraryBorrowBookCopyApiView,LibraryReturnBookCopyApiView

urlpatterns = [
    path("", LibraryListCreateView.as_view(), name="library_list_create"),
    path("<int:pk>/", LibraryUpdateView.as_view(), name="library_update"),

    path("add-book/<int:library_id>/", LibraryAddBookApiView.as_view(), name="library_add_book"),
    path("borrow-book/<int:library_id>/", LibraryBorrowBookApiView.as_view(), name="library_borrow_book"),
    path("borrow-book-copy/<int:library_id>", LibraryBorrowBookCopyApiView.as_view(), name="library_borrow_book_copy"),

    path("return-book/<int:library_id>", LibraryReturnBookCopyApiView.as_view(), name="library_return_book"),
]