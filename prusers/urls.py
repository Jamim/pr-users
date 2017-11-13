from django.conf.urls import url, include


urlpatterns = [
    url(r'^api/auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/signup/', include('users.signup_urls', namespace='signup')),
    url(r'^api/users/', include('users.urls', namespace='users')),
]
