from django.contrib import admin
from quizzes.models import Quiz, Question, Answer

def download_as_csv(modeladmin, request, queryset):
    import csv
    file = open(f'{queryset.first().__class__.__name__.lower()}.csv', 'w')
    writer = csv.writer(file, delimiter=';')
    writer.writerow(modeladmin.list_display)
    for row in queryset:
        writer.writerow([getattr(row, field) for field in modeladmin.list_display])

class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created",
    )
    list_filter = ("name",)
    ordering = ("name", "modified", "created")
    search_fields = (
        "name",
    )
    actions = [download_as_csv]

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
    list_filter = ("content",)
    ordering = ("content", "quiz", "created")
    search_fields = (
        "content",
    )
    inlines = (
        AnswerInline,
    )
    actions = [download_as_csv]

admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "content",
        "is_correct",
        "created",
    )
    list_filter = ("content", "is_correct")
    ordering = ("content", "is_correct", "question", "created")
    search_fields = (
        "content",
    )
    actions = [download_as_csv]

admin.site.register(Answer, AnswerAdmin)


