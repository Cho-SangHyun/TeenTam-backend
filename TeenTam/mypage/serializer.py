from rest_framework import serializers
from account.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone

# 마이페이지 메인 화면


class MypageMainSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['username', 'email', 'profile_image', 'first_name', 'last_name',
                  'boards_written', 'comments_written']


class ChangePasswordSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    class Meta:

        model = User
        fields = ['password', 'user_id', 'new_password']

    def validate(self, data):

        user_id = data["user_id"]
        password = data["password"]
        user = User.objects.get(id=user_id)

        if not check_password(password, user.password):
            # wrong password (기존 비밀번호 오류)
            raise serializers.ValidationError("wrong password")

        new_password = data["new_password"]
        user.set_password(new_password)
        user.save()

        return super().validate(data)


class ChangeUsernameDatetimeSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['username_is_changed']


class ChangeUsernameSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['username']

    def validate(self, data):

        user_id = data.get('user_id')
        datetime = data.get('datetime')
        user = User.objects.get(id=user_id)

        if not datetime > user.username_is_changed:
            # 최근 변경날짜 30일 미만이므로 변경 불가
            raise serializers.ValidationError(
                "not allowed to change username until 30days from latest change")

        new_username = data["new_username"]
        user.username = new_username

        # 변경 가능한 날짜 한달 후로 갱신
        user.username_is_changed = timezone.now() + timezone.timedelta(days=30)
        user.save()

        return super().validate(data)


# 회원정보 수정
class ModifyUserInformationSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['last_name', 'first_name',  
                  'phone_number', 'postcode', 'address', 'detail_address', 'grade']
