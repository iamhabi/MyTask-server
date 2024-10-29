from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import MyUser
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer, ChangePasswordSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = RegisterSerializer


class ChangePasswordView(UpdateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer