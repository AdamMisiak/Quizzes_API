from django.contrib import admin

from .models import QuizInvitation, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name")


admin.site.register(User, UserAdmin)


class QuizInvitationAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "invited", "quiz", "status", "created")
    list_filter = ("quiz", "status")
    ordering = ("owner", "invited", "quiz", "status", "created")
    search_fields = ("quiz__name", "owner__first_name", "owner__last_name", "invited__first_name", "invited__last_name")


admin.site.register(QuizInvitation, QuizInvitationAdmin)
