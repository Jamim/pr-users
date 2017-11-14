from django.conf.urls import url, include


urlpatterns = [
    url(r'^api/auth/', include('users.auth_urls', namespace='auth')),
    url(r'^api/users/', include('users.urls', namespace='users')),
]
