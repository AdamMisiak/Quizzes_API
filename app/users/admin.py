from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
    )
    list_filter = ("email", "first_name", "last_name")
    ordering = ("email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name")


admin.site.register(User, UserAdmin)
