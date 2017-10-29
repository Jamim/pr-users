from rest_framework import generics, permissions

from django.contrib.auth import get_user_model

from .permissions import IsNotCurrentUser
from .serializers import UserSerializer


user_model = get_user_model()


class UserViewMixin(object):
    serializer_class = UserSerializer
    queryset = (
        user_model.objects.exclude(is_superuser=True).exclude(is_staff=True)
    )


class UserList(UserViewMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)


class UserView(UserViewMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsNotCurrentUser)
