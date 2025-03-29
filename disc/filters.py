import django_filters
from .models import Disc
from django.db.models import Q
from .constants import COLOR_CHOICES

class DiscFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_disc_query', label='Search')
    color = django_filters.ChoiceFilter(choices=COLOR_CHOICES, lookup_expr='iexact')
    has_reward = django_filters.BooleanFilter(method='filter_has_reward', label='Has Reward')

    class Meta:
        model = Disc
        fields = ['type', 'mold_name', 'manufacturer', 'color', 'status', 'notes', 'has_reward']

    def filter_disc_query(self, queryset, name, value):
        return queryset.filter(
            Q(type__icontains=value) |
            Q(mold_name__icontains=value) |
            Q(manufacturer__name__icontains=value) |
            Q(color__icontains=value) |
            Q(status__icontains=value) |
            Q(notes__icontains=value)
        )

    def filter_has_reward(self, queryset, name, value):
        if value:
            return queryset.filter(reward__isnull=False)
        return queryset
