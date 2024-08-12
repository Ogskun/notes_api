from rest_framework import serializers

from django.contrib.auth.models import User
from django.core.validators import (
    RegexValidator, 
)

from core.models import (
    Note, 
    UserInfo, 
)


class NoteSerializer(serializers.ModelSerializer):
    date_created = serializers.DateField(
        read_only=True,
        format='%m-%d-%Y'
    )

    class Meta:
        model = Note
        exclude = [
            'is_deleted', 
            'user',
        ]


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = [
            'username',
            'name',
            'email',
            'password',
            'confirm_password', 
        ]

    username = serializers.CharField(source='user.username', required=True)
    name = serializers.CharField(required=True)
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(
        required=True, 
        write_only=True, 
        validators=[
            RegexValidator(
                '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[#?!@$%^&*-]).{8,}$',
                message=(
                    'Password must contain at least 8 characters, including '
                    'uppercase, lowercase, and special characters.'
                )
            )
        ]
    )
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value, is_active=True).exists():
            raise serializers.ValidationError('Username already taken.')
        
        return value

    def validate_confirm_password(self, value):
        if value != self.initial_data.get('password'):
            raise serializers.ValidationError(
                "Confirm password doesn't match."
            )
        
        return value

    def save(self):
        # Access validated data
        username = self.validated_data['user']['username']
        email = self.validated_data['user']['email']
        password = self.validated_data['password']
        name = self.validated_data['name']

        # Create user instance
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        user.is_active = True
        user.save()

        # Update UserInfo instance
        userinfo = UserInfo.objects.get(user=user)
        userinfo.name = name
        userinfo.save()

        return userinfo