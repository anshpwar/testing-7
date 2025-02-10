from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("gradebook/", include("grading.urls")),
    path("entries/", include("enrollments.urls")),
]
