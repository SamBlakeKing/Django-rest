from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snipple
from snippets.serializers import SnippetSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer, TeamUserSerializer, StuUserSerializer
from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ParseError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from snippets.models import MyUser, TeamUser, StuUser

import logging
import snippets

# Create your views here.

# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

#
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     if request.method == 'GET':
#         snippets = Snipple.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     try:
#         snippet = Snipple.objects.get(pk=pk)
#     except Snipple.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class SnippetList(APIView):
#     def get(self, request, format=None):
#         snippets = Snipple.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SnippetDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Snipple.objects.get(pk=pk)
#         except Snipple.DoesNotExist:
#             return Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snipple.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snipple.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format),
#     })
#
# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snipple.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)
#
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)

class AuthView(APIView):
    def get(self, request):
        return Response({'detail':'GET Response'})

    def post(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invaild JSON - {0}'.format(error.detail),
                            status=status.HTTP_400_BAD_REQUEST)

        if "username" not in data or "password" not in data:
            return Response('Wrong Credentials', status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            return Response('Wrong user or password', status=status.HTTP_403_FORBIDDEN)

        token = Token.objects.get_or_create(user=user)
        return Response({'detail': "POST answer", 'token':token[0].key})

class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    def change_password(self, userId, request):
        if not userId:
            return Response('Update failed', status=status.HTTP_403_FORBIDDEN)

        if 'password' in request.data:
            password = request.data['password']
        else:
            password = '123456'

        user = MyUser.objects.get(pk=userId)
        user.set_password(password)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        userId = super(UserViewSet,self).create(request, *args, **kwargs).data['id']
        return self.change_password(userId, request)

    def update(self, request, *args, **kwargs):
        userId = super(UserViewSet, self).update(request, *args, **kwargs).data['id']
        return self.change_password(userId, request)

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snipple.objects.all()
    serializer_class = SnippetSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, snippets.permissions.IsOwnerOrReadOnly)

    @detail_route(renderer_class=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        raw_token = self.request.META.get('HTTP_AUTHORIZATION')
        token = raw_token.split(' ')[-1]
        userId = Token.objects.get(key=token).user_id

        user = MyUser.objects.get(pk=userId)
        serializer.save(owner=user)

class TeamUserViewSet(viewsets.ModelViewSet):
    queryset = TeamUser.objects.all()
    serializer_class = TeamUserSerializer

    def change_password(self, userId, request):
        if not userId:
            return Response('Update failed', status=status.HTTP_403_FORBIDDEN)

        if 'password' in request.data:
            password = request.data['password']
        else:
            password = '123456'

        user = TeamUser.objects.get(pk=userId)
        user.set_password(password)
        user.save()
        serializer = TeamUserSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        userId = super(TeamUserViewSet,self).create(request, *args, **kwargs).data['id']
        return self.change_password(userId, request)

    def update(self, request, *args, **kwargs):
        userId = super(TeamUserViewSet, self).update(request, *args, **kwargs).data['id']
        return self.change_password(userId, request)

class StuUserViewSet(viewsets.ModelViewSet):
    queryset = StuUser.objects.all()
    serializer_class = StuUserSerializer

    def change_password(self, userId, request):
        if not userId:
            return Response('Update failed', status=status.HTTP_403_FORBIDDEN)

        if 'password' in request.data:
            password = request.data['password']
        else:
            password = '123456'

        user = StuUser.objects.get(pk=userId)
        user.set_password(password)
        user.save()
        serializer = StuUserSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        userId = super(StuUserViewSet,self).create(request, *args, **kwargs).data['id']
        return self.change_password(userId, request)

    def update(self, request, *args, **kwargs):
        userId = super(StuUserViewSet, self).update(request, *args, **kwargs).data['id']
        return self.change_password(userId, request)

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
    })