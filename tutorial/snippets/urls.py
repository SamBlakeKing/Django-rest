from django.conf.urls import url, patterns
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from snippets.views import SnippetViewSet, UserViewSet, TeamUserViewSet, StuUserViewSet

# urlpatterns = [
#     url(r'^snippets/$', views.snippet_list),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# ]

# urlpatterns = [
#     url(r'^snippets/$', views.SnippetList.as_view()),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
#     url(r'^usrs/$', views.UserList.as_view()),
#     url(r'^usrs/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
#     # url(r'^$', views.api_root),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)
#
# urlpatterns += [
#     url(r'^api-auth/',include('rest_framework.urls',
#                               namespace='rest_framework')),
# ]

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
})
user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

teamuser_list = TeamUserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

teamuser_detail = TeamUserViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

stuuser_list = StuUserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

stuuser_detail = StuUserViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns(patterns('snippets.views',
    url(r'^$', views.api_root),
    url(r'^snippets/$', snippet_list, name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^teamusers/$', teamuser_list, name='teamuser-list'),
    url(r'^teamusers/(?P<pk>[0-9]+)/$', teamuser_detail, name='teamuser-detail'),
    url(r'^stuusers/$', stuuser_list, name='stuuser-list'),
    url(r'^stuusers/(?P<pk>[0-9]+)/$', stuuser_detail, name='stuuser-detail'),
))

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', views.AuthView.as_view()),
]

# from snippets import views
# from rest_framework.routers import DefaultRouter
#
# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
# router.register(r'users', views.UserViewSet)
#
# # The API URLs are now determined automatically by the router.
# # Additionally, we include the login URLs for the browseable API.
# urlpatterns = patterns('',
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# )