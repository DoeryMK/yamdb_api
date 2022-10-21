from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """Фильтры для произведений."""

    genre = filters.CharFilter(field_name="genre__slug")
    category = filters.CharFilter(field_name="category__slug")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    year = filters.NumberFilter(field_name="year")

    class Meta:
        model = Title
        fields = ["genre", "category", "name", "year"]
