from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import check_password, make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'school', 'grade']


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'birth', 'phone_number']
        # fields += ['postcode', 'address','detail_address', 'phone_number'] # 추가 기입 사항

    def validate(self, data):

        # 이메일 중복 확인
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("user email already exists")

        # 전화번호 중복 확인
        phone_number = data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                "user phone number already exists")

        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(SignupSerializer, self).create(validated_data)


class UsernameSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username']

    def validate(self, data):

        username = data["username"]
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("username already exists")

        return data


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):

        email = data["email"]
        password = data["password"]

        if email is None or password is None:
            # blank email or password
            raise serializers.ValidationError("email / password required")

        user = User.objects.filter(email=email).first()

        if user is None:
            # not registered email
            raise serializers.ValidationError("not registered user")

        if not check_password(password, user.password):
            # wrong password
            raise serializers.ValidationError("wrong password")

        return data


# 이메일 찾기
class FindEmailSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=True, write_only=True)

    class Meta:

        model = User
        fields = ["phone_number", "birth"]

    def validate(self, data):

        # 전화번호와 생년월일로 식별
        ph_num = data["phone_number"]
        birth = data["birth"]

        user = User.objects.filter(phone_number=ph_num).first()

        if user is None:
            # 등록된 전화번호 없음
            raise serializers.ValidationError("not registered phone number")

        if user.birth is not birth:
            # 전화번호, 생년월일 불일치
            raise serializers.ValidationError("wrong birth")

        return data


# 비밀번호 찾기
class FindPasswordSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=True, write_only=True)

    class Meta:

        model = User
        fields = ["email", "birth"]

    def validate(self, data):

        # 이메일과 생년월일로 식별
        email = data["email"]
        birth = data["birth"]
        user = User.objects.filter(email=email, birth=birth).first()

        if user is None:
            raise serializers.ValidationError("not registered email")

        if user.birth != birth:
            raise serializers.ValidationError("wrong birth")

        return data
