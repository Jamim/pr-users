from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


from django.contrib.auth import get_user_model, authenticate, login, logout

from .permissions import IsNotCurrentUser, IsNotAuthenticated
from .serializers import UserSerializer, NewUserSerializer, CredentialsSerializer


user_model = get_user_model()


class UserViewMixin(object):
    queryset = (
        user_model.objects.exclude(is_superuser=True)
                          .exclude(is_staff=True)
                          .order_by('id')
    )


class UserList(UserViewMixin, generics.ListCreateAPIView):
    serializer_class = NewUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserView(UserViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsNotCurrentUser)


class SignUpView(generics.CreateAPIView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = NewUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(generics.GenericAPIView):
    serializer_class = CredentialsSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            login(request, user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
