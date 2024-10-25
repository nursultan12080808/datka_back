import django_filters
from shark_app.models import News

class NewsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  # Нечувствительный к регистру и частичное совпадение

    class Meta:
        model = News
        fields = ["category", "tags", "user", "location", "rating", "name"]