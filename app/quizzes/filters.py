from django.db.models import Q
from django_filters import CharFilter, FilterSet

from .models import Quiz


class QuizFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains", distinct=True)
    # first_name = CharFilter(field_name="owner__first_name", lookup_expr="icontains", distinct=True)
    # last_name = CharFilter(field_name="owner__last_name", lookup_expr="icontains", distinct=True)
    question = CharFilter(field_name="questions__content", lookup_expr="icontains", distinct=True)
    answer = CharFilter(field_name="questions__answers__content", lookup_expr="icontains", distinct=True)
    search = CharFilter(method="search_filter")

    class Meta:
        model = Quiz
        fields = [
            "search",
        ]

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            # | Q(owner__first_name__icontains=value)
            # | Q(owner__last_name__icontains=value)
            | Q(questions__content__icontains=value)
            | Q(questions__answers__content__icontains=value)
        ).distinct()
