from snippets.models import Snipple, LANGUAGE_CHOINCES, STYLE_CHOICES, MyUser, TeamUser, StuUser
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
        model = TeamUser
        fields = ('id', 'email', 'name', 'snippets')

class TeamUserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snipple)

    class Meta:
        model = TeamUser
        fields = ('id', 'email', 'name', 'snippets')

class StuUserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snipple)

    class Meta:
        model = StuUser
        fields = ('id', 'email', 'name', 'snippets')