from django.contrib import admin

from proverator_app.models import Domain, Request


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("domain",)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("domain","status_code","response_time","verified_at")
