from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']


class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'birth', 'postcode',
                'address','detail_address', 'phone_number']

    def save(self, request):
        
        user = super().save()
        user.set_password(self.validated_data['password'])
        user.save()

        return user
    
    def validate(self, data):
        
        username = data.get('username')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("user already exists")

        return data        

class LoginSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required = True, write_only = True)
    password = serializers.CharField(
        required = True,
        write_only = True,
        style={'input_type' : 'password'},
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):

        id = data.get('id')
        password = data.get('password')

        if User.objects.filter(id=id).exists():
            user = User.objects.get(id=id)

            if not check_password(password, user.username):
                raise serializers.ValidationError("wrong password")
        
        else:
            raise serializers.ValidationError("not registered user")
        
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'user' : user,
            'refresh' : refresh,
            'access' : access,
        }

        return data