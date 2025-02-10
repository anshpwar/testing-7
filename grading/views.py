from django.http import Http404
from django.shortcuts import render

from courses.models import Course

from . import services


def gradebook(request, code):
    try:
        course = Course.objects.get(code=code)
    except Course.DoesNotExist:
        raise Http404("unknown course")
    grades = list(course.grades.all())
    size = services.page_size(len(grades))
    page = max(1, int(request.GET.get("page", "1")))
    rows = grades[(page - 1) * size:page * size]
    return render(request, "grading/gradebook.html", {"course": course, "rows": rows, "page": page, "page_size": size})
