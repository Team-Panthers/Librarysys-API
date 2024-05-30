from django.urls import path

from .views import LibraryListCreateView,LibraryUpdateView,LibraryAddBookApiView,LibraryBorrowBookApiView,LibraryBorrowBookCopyApiView,LibraryReturnBookCopyApiView,LibraryUsersList,LibraryUserRetrieve,LibraryAdminRetrieveDeleteBook,LibraryAdminRetrieveDeleteBookCopy

urlpatterns = [
    # library create and edit
    path("", LibraryListCreateView.as_view(), name="library_list_create"),
    path("<int:pk>/", LibraryUpdateView.as_view(), name="library_update"),

    # library admin endpoints for books and book copy operation
    path("add-book/<int:library_id>/", LibraryAddBookApiView.as_view(), name="library_add_book"),
    path("borrow-book/<int:library_id>/", LibraryBorrowBookApiView.as_view(), name="library_borrow_book"),
    path("borrow-book-copy/<int:library_id>/", LibraryBorrowBookCopyApiView.as_view(), name="library_borrow_book_copy"),
    path("return-book/<int:library_id>/", LibraryReturnBookCopyApiView.as_view(), name="library_return_book"),
    path("book/<int:library_id>/<int:pk>/", LibraryAdminRetrieveDeleteBook.as_view(), name="library_book_retrieve_delete"),
    path("book-copy/<int:library_id>/<int:pk>/", LibraryAdminRetrieveDeleteBookCopy.as_view(), name="library_book_copy_retrieve_delete"),
    
    # library admin endpoint for users
    path("users/<int:library_id>/", LibraryUsersList.as_view(), name="library_users"),
    path("user/<int:library_id>/<int:pk>/", LibraryUserRetrieve.as_view(), name="library_user"),

]