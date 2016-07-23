from snippets.models import Snipple, LANGUAGE_CHOINCES, STYLE_CHOICES
from rest_framework import serializers
from django.contrib.auth.models import User

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snipple
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snipple)

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')