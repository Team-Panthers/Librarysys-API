from django.urls import path

from .views import LibraryListCreateView,LibraryUpdateView,LibraryAddBookApiView,LibraryBorrowBookApiView,LibraryBorrowBookCopyApiView,LibraryReturnBookCopyApiView,LibraryAvailableBookList,LibraryAllBookList,LibraryAllBookCopies,LibraryAvailableBookCopies,LibraryBookGetBookCopies,LibraryUsersList,LibraryUserRetrieve,LibraryAdminUpdateDeleteBook,LibraryAdminUpdateDeleteBookCopy

urlpatterns = [
    path("", LibraryListCreateView.as_view(), name="library_list_create"),
    path("<int:pk>/", LibraryUpdateView.as_view(), name="library_update"),

    path("add-book/<int:library_id>/", LibraryAddBookApiView.as_view(), name="library_add_book"),
    path("borrow-book/<int:library_id>/", LibraryBorrowBookApiView.as_view(), name="library_borrow_book"),
    path("borrow-book-copy/<int:library_id>/", LibraryBorrowBookCopyApiView.as_view(), name="library_borrow_book_copy"),

    path("return-book/<int:library_id>/", LibraryReturnBookCopyApiView.as_view(), name="library_return_book"),

    path("available-books/<int:library_id>/", LibraryAvailableBookList.as_view(), name="library_book_list"),
    path("all-books/<int:library_id>/", LibraryAllBookList.as_view(), name="library_all_book_list_and_search"),
    path("book-copies/<int:library_id>/<int:pk>/", LibraryBookGetBookCopies.as_view(), name="library_get_bookcopies_for_book"),
    path("book/<int:library_id>/<int:pk>/", LibraryAdminUpdateDeleteBook.as_view(), name="library_book_retrieve_delete"),
    
    path("available-book-copies/<int:library_id>/", LibraryAvailableBookCopies.as_view(), name="library_available_book_copies"),
    path("all-book-copies/<int:library_id>/", LibraryAllBookCopies.as_view(), name="library_all_book_copies"),
    path("book-copy/<int:library_id>/<int:pk>/", LibraryAdminUpdateDeleteBookCopy.as_view(), name="library_book_copy_retrieve_delete"),
    
    
    path("users/<int:library_id>/", LibraryUsersList.as_view(), name="library_users"),
    path("user/<int:library_id>/<int:pk>/", LibraryUserRetrieve.as_view(), name="library_user"),

]