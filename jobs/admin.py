from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("kind", "status", "attempts", "run_after")
    list_filter = ("status", "kind")
