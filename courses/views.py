from django.http import Http404, JsonResponse
from django.shortcuts import render

from .models import Course


def course_list(request):
    return render(request, "courses/course_list.html", {"courses": Course.objects.filter(active=True)})


def course_detail(request, code):
    try:
        course = Course.objects.prefetch_related("lessons").get(code=code, active=True)
    except Course.DoesNotExist:
        raise Http404("unknown course")
    return render(request, "courses/course_detail.html", {"course": course, "lessons": course.lessons.all(),
                                                          "total_minutes": course.total_minutes()})


def course_json(request):
    rows = [{"code": c.code, "title": c.title, "credits": c.credits} for c in Course.objects.filter(active=True)]
    return JsonResponse({"courses": rows})
