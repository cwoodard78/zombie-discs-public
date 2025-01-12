import django_filters
from .models import Disc
from django.db.models import Q

class DiscFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_disc_query', label='Search')

    class Meta:
        model = Disc
        fields = ['type', 'mold_name', 'manufacturer', 'color', 'status', 'notes']

    def filter_disc_query(self, queryset, name, value):
        return queryset.filter(
            Q(type__icontains=value) |
            Q(mold_name__icontains=value) |
            Q(manufacturer__name__icontains=value) |  # Foreign key
            Q(color__icontains=value) |
            Q(status__icontains=value) |
            Q(notes__icontains=value)
        )
