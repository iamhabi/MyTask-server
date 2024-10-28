from typing import Any, Dict
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .models import MyUser


# return user id with token
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user_id"] = str(user.id)

        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data["user_id"] = str(self.user.id)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
    )

    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = MyUser
        fields = ['username', 'password1', 'password2', 'email']
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match."})
    
        return attrs
    
    def create(self, validated_data):
        user = MyUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
        )

        user.save()

        return user