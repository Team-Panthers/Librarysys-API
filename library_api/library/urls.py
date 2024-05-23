from django.urls import path

from .views import LibraryListCreateView,LibraryUpdateView

urlpatterns = [
    path("", LibraryListCreateView.as_view(), name="library_list_create"),
    path("<int:pk>/", LibraryUpdateView.as_view(), name="library_update"),
]