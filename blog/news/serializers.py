from rest_framework import serializers
from news.models import News


class NewsSerializer (serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_published = serializers.HiddenField(default=False)

    class Meta:
        model = News
        fields = ('id', 'title', 'category', 'url', 'is_published', 'time_create', 'user')

