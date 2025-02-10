from django.urls import path

from . import views

urlpatterns = [
    path("", views.course_list, name="course-list"),
    path("json/", views.course_json, name="course-json"),
    path("<str:code>/", views.course_detail, name="course-detail"),
]
