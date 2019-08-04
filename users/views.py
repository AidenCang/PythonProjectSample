import re
from random import choice

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import mixins, viewsets, status, permissions, authentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.views import JSONWebTokenAPIView

from ProjectSmaple.settings import REGEX_EMAIL
from users.models import VerifyCode
from users.serializers import CodeSerializer, UserRegisterSerializer, UserDetailSerializer, \
    CustomJSONWebTokenSerializer, ResetPassWordSerializer

User = get_user_model()


# Create your views here.
class CustomBackend(ModelBackend):
    """
    自定义用户验证:用户名或者手机号登陆，并且在setting中配置
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # user = User.objects.get(Q(username=username) | Q(mobile=username))
            user = User.objects.get(Q(username=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = CustomJSONWebTokenSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    # serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = [JSONWebTokenAuthentication, authentication.SessionAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    # 返回当前用户
    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        else:
            return []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegisterSerializer
        else:
            return UserDetailSerializer


class CodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
       通过电话号码/邮件获取六位的验证码

       支持的国家:

        1.中国
        2.任意邮箱格式

       create：
           获取验证码
       """

    serializer_class = CodeSerializer

    def generate_code(self):
        """
        生成六位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))
        return "".join(random_str)

    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['mobile']

        code = self.generate_code()
        registerType = ""
        print('验证码: ' + code)

        # 使用电话号码注册
        if re.match(REGEX_EMAIL, username) is not None:
            # 发送短信验证码
            registerType = 'mobile'
            pass

        # 使用邮件注册
        if re.match(REGEX_EMAIL, username) is not None:
            # 发送永久验证码
            registerType = 'email'
            # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
            send_mail('Subject here', '欢迎注册ProjectSample，验证码 {0}'.format(code), 'projectsample@163.com',
                      ['projectsample@163.com'], fail_silently=False)

        code_record = VerifyCode(code=code, mobile=username)
        code_record.save()
        return Response({
            "type": registerType,
            "username": username,
            "code": code
        }, status=status.HTTP_201_CREATED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RestPasswd(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ResetPassWordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.get(Q(mobile=username) | Q(email=username))
        user.set_password(serializer.validated_data["password"])
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
