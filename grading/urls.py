from django.urls import path

from . import views

urlpatterns = [path("<str:code>/", views.gradebook, name="gradebook")]
