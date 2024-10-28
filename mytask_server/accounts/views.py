from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import MyUser
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = RegisterSerializer
