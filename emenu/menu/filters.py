from django_filters.rest_framework import FilterSet, CharFilter, DateTimeFilter


from menu.models import Menu


class MenuFilterSet(FilterSet):
    """MenuFilterSet"""
    name = CharFilter(field_name='name', lookup_expr='contains')
    created = DateTimeFilter(field_name='created', lookup_expr='exact')
    created__lte = DateTimeFilter(field_name='created', lookup_expr='lte')
    created__gte = DateTimeFilter(field_name='created', lookup_expr='gte')
    updated = DateTimeFilter(field_name='updated', lookup_expr='exact')
    updated__lte = DateTimeFilter(field_name='updated', lookup_expr='lte')
    updated__gte = DateTimeFilter(field_name='updated', lookup_expr='gte')

    class Meta:
        """Meta"""
        model = Menu
        fields = ['name']
