import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from ProjectSmaple.settings import REGEX_MOBILE, REGEX_EMAIL
from datetime import datetime, timedelta

from users.models import VerifyCode

User = get_user_model()
EMAIL = 'email'
MOBILE = 'mobile'


class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    """
    自定义用户验证方式，判断传递的内容是否是邮箱或电话号
    """

    def validate_username(self, username):
        # 判断用户名是邮箱还是电话号码
        if not re.match(REGEX_EMAIL, username) and not re.match(REGEX_MOBILE, username):
            raise serializers.ValidationError('用户名不是邮箱或者电话号码')
        return username


# 序列化器处理多一个字段和少一个字段
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'birthday', 'gender', 'mobile', 'email')


# 序列化器处理多一个字段和少一个字段
class ResetPassWordSerializer(serializers.ModelSerializer):
    # 客户端提交多余的字段
    code = serializers.CharField(required=True, max_length=6, min_length=6, write_only=True, label='验证码',
                                 help_text='验证码')
    username = serializers.CharField(required=True, max_length=50, write_only=True, label='账号',
                                     help_text='账号')
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def create(self, validated_data):
        pass

    class Meta:
        model = User
        fields = ('code', 'username',  'password')


# 序列化器处理多一个字段和少一个字段
class UserRegisterSerializer(serializers.ModelSerializer):
    # 客户端提交多余的字段
    code = serializers.CharField(required=True, max_length=6, min_length=6, write_only=True, label='验证码',
                                 help_text='验证码')
    type = serializers.CharField(required=True, write_only=True, help_text='注册类型:mobile、email', label='类型')
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        verify_records = None
        if self.initial_data["type"] == "mobile":
            verify_records = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        elif self.initial_data["type"] == "email":
            verify_records = VerifyCode.objects.filter(mobile=self.initial_data["email"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate_type(self, code):
        register_type = self.initial_data["type"]
        if register_type != "mobile" and register_type != "email":
            raise serializers.ValidationError('注册类型必须是mobile or email')

    def validate(self, attrs):

        # 验证是不是手机号和邮件
        if not attrs['email'] and not attrs['mobile']:
            raise serializers.ValidationError('用户名不是邮箱或者电话号码')
        # 处理提交的数据到对应数据库
        if attrs["mobile"]:
            attrs["username"] = attrs["mobile"]
        elif attrs["email"]:
            attrs["username"] = attrs["email"]
        del attrs["code"]
        del attrs["type"]
        return attrs

    def validate_mobile(self, mobile):
        # 电话号码不为空，才验证
        if mobile and re.match(REGEX_MOBILE, mobile) is None:
            raise serializers.ValidationError('电话号码错误!!!!')
        return mobile

    def validate_email(self, email):
        # 电话号码不为空，才验证
        if email and re.match(REGEX_EMAIL, email) is None:
            raise serializers.ValidationError('邮件格式错误!!!!')
        return email

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('code', 'type', 'mobile', 'email', 'password')


class CodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=50, help_text='电话号码或邮箱', label='电话号码或邮箱')
    code_type = serializers.CharField(required=False, max_length=50, help_text='register,None', label='后期验证码类型')

    def validate_mobile(self, mobile):
        codetype = self.initial_data['code_type']

        if codetype == "register":  # 只有注册才能去验证用户是否存在

            # 验证是不是手机号和邮件
            if not re.match(REGEX_EMAIL, mobile) and not re.match(REGEX_MOBILE, mobile):
                raise serializers.ValidationError('用户名不是邮箱或者电话号码')

            # 使用电话号码注册
            if not re.match(REGEX_EMAIL, mobile):
                if User.objects.filter(mobile=mobile).count():
                    raise serializers.ValidationError('用户已存在!!!!')

            # 使用邮件注册
            if not re.match(REGEX_EMAIL, mobile):
                if User.objects.filter(email=mobile).count():
                    raise serializers.ValidationError('用户已存在!!!!')

        # 验证码时间
        one_minites_age = datetime.now() - timedelta(hours=0, minutes=0, seconds=10);
        if VerifyCode.objects.filter(add_time__gt=one_minites_age, mobile=mobile):
            raise serializers.ValidationError('验证码点击太频繁!!!!')

        # 验证完成之后开始发送短信

        return mobile

    # def validate(self, attrs):
    #     del attrs['code_type']
    #     return attrs
