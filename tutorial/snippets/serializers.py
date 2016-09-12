from snippets.models import Snipple, LANGUAGE_CHOINCES, STYLE_CHOICES, MyUser
from rest_framework import serializers
from django.contrib.auth.models import User

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = Snipple
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snipple)

    class Meta:
        model = MyUser
        fields = ('id', 'email', 'name', 'snippets')