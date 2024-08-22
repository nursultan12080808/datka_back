import django_filters

from shark_app.models import *

class NewsFilter(django_filters.FilterSet):
    class Meta:
        model = News
        fields = ["category", "tags", "user", "location", "rating"]