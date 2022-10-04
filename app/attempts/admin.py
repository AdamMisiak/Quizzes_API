from django.contrib import admin

from .models import Attempt, AttemptAnswer


class AttemptAnswerInline(admin.StackedInline):
    model = AttemptAnswer
    extra = 0


class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "quiz",
        "is_finished",
        "is_successful",
        "created",
    )
    ordering = ("is_finished", "is_successful", "user", "quiz", "modified", "created")
    search_fields = ("user__email", "user__first_name", "user__last_name", "quiz__name")
    inlines = (AttemptAnswerInline,)


admin.site.register(Attempt, AttemptAdmin)


class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "attempt",
        "question",
        "answer",
        "is_correct",
        "created",
    )
    ordering = ("attempt", "question", "answer", "created")
    search_fields = ("question__content", "answer__content", "attempt__quiz__name")


admin.site.register(AttemptAnswer, AttemptAnswerAdmin)
