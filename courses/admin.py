from django.contrib import admin

from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ("code", "title", "credits", "active")
