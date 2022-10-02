from django.contrib import admin
from import_export.admin import ExportActionMixin
from quizzes.models import Answer, Question, Quiz


class QuizAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "created",
    )
    list_filter = ("name", "created")
    ordering = ("name", "owner", "modified", "created")
    search_fields = ("name", "owner")


admin.site.register(Quiz, QuizAdmin)


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "quiz",
        "content",
        "created",
    )
    list_filter = ("created",)
    ordering = ("content", "quiz", "created")
    search_fields = ("content",)
    inlines = (AnswerInline,)


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "content",
        "is_correct",
        "created",
    )
    list_filter = ("is_correct", "created")
    ordering = ("content", "is_correct", "question", "created")
    search_fields = ("content",)


admin.site.register(Answer, AnswerAdmin)
