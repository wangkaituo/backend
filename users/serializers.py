from rest_framework import serializers
from .models import EmpUser


class EmpUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    department_name = serializers.ReadOnlyField(source='department.dept_name')

    class Meta:
        model = EmpUser
        fields = [
            'emp_id', 'emp_name', 'emp_email', 'emp_phone',
            'emp_role', 'emp_join_date', 'department', 'department_name', 'password'
        ]
        read_only_fields = ('emp_id', 'emp_join_date')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = EmpUser(**validated_data)
        user.set_password(password)  # 加密处理
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # 加密处理
        instance.save()
        return instance


class ChangeEmpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpUser
        fields = ['emp_name', 'emp_email', 'emp_phone', 'emp_role', 'department']
        read_only_fields = ('emp_id', 'emp_join_date')