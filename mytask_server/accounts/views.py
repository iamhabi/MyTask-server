from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import MyUser
from .permissions import UserPermission
from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [UserPermission,]
    serializer_class = RegisterSerializer


class DeleteView(DestroyAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [UserPermission,]


class ChangePasswordView(UpdateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [UserPermission,]
    serializer_class = ChangePasswordSerializer


class UpdateView(UpdateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [UserPermission,]
    serializer_class = UpdateUserSerializer