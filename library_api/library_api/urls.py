
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("user.urls")),

    path("api/library/", include("library.urls")),
    path("api/book/", include("book.urls")),
]
