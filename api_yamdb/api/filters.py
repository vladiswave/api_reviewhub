from django_filters import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр для произведений."""
    category_slug = CharFilter(
        field_name='category__slug',
        lookup_expr='exact'
    )
    genre_slug = CharFilter(
        field_name='genre__slug',
        lookup_expr='exact'
    )
    name = CharFilter(lookup_expr='icontains')
    year = NumberFilter()

    class Meta:
        model = Title
        fields = ['category_slug', 'genre_slug', 'name', 'year']
