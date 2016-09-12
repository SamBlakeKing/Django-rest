from rest_framework import permissions
from rest_framework.authtoken.models import Token
from snippets.models import MyUser

import logging

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        raw_token = request.META.get('HTTP_AUTHORIZATION')
        token = raw_token.split(' ')[-1]
        userId = Token.objects.get(key=token).user_id
        user = MyUser.objects.get(pk=userId)

        return obj.owner == user