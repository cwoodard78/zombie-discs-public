"""
DiscFilter for Advanced Search

This filter class powers the disc search form, allowing users to search by various fields including type, mold name, manufacturer, color, reward status, and a general text query.
"""

import django_filters
from .models import Disc
from django.db.models import Q
from .constants import COLOR_CHOICES

class DiscFilter(django_filters.FilterSet):
    # General search field that applies to multiple fields
    query = django_filters.CharFilter(method='filter_disc_query', label='Search')
    # Case-insensitive exact match for predefined color choices
    color = django_filters.ChoiceFilter(choices=COLOR_CHOICES, lookup_expr='iexact')
    # Custom boolean filter to check whether the disc has a reward
    has_reward = django_filters.BooleanFilter(method='filter_has_reward', label='Has Reward')

    class Meta:
        model = Disc
        fields = ['type', 'mold_name', 'manufacturer', 'color', 'status', 'notes', 'has_reward']

    def filter_disc_query(self, queryset, name, value):
        """
        Filters the queryset based on a broad search across multiple fields.
        """
        return queryset.filter(
            Q(type__icontains=value) |
            Q(mold_name__icontains=value) |
            Q(manufacturer__name__icontains=value) |
            Q(color__icontains=value) |
            Q(status__icontains=value) |
            Q(notes__icontains=value) |
            Q(user__username__icontains=value)
        )

    def filter_has_reward(self, queryset, name, value):
        """
        Filters discs based on whether they have an associated reward.
        """
        if value:
            return queryset.filter(reward__isnull=False)
        return queryset
