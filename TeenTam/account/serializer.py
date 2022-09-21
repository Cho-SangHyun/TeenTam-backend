from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']


class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'birth']
        # fields += ['postcode', 'address','detail_address', 'phone_number'] # 추가 기입 사항

    def validate(self, data):
        
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("user name already exists")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("user email already exists")

        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(SignupSerializer, self).create(validated_data)

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