from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.decorators import permission_classes, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import EmpUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 添加字段声明
    emp_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        # 修改获取字段的方式
        emp_id = attrs.get(self.username_field)
        password = attrs.get('password')
        try :
            user = EmpUser.objects.get(emp_id=emp_id)
        except EmpUser.DoesNotExist:
            raise serializers.ValidationError("用户不存在")
        if not user.check_password(password):
            raise serializers.ValidationError("密码错误")
        if not user.is_active:
            raise serializers.ValidationError("用户已被禁用")
        data = super().validate(
            {
                'emp_id': user.emp_id,
                'password': password,
            }
        )
        data['emp_id'] = user.emp_id
        data['role'] = user.emp_role
        return data
@permission_classes([])
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer