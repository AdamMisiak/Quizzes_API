from django.contrib import admin

from .models import Attempt


class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "quiz",
    )
    ordering = ("user", "quiz", "modified", "created")
    search_fields = ("user__email", "user__first_name", "user__last_name", "quiz__name")


admin.site.register(Attempt, AttemptAdmin)
