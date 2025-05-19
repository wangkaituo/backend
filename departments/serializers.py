from rest_framework import serializers
from users.models import EmpUser
from.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    dept_manager_name = serializers.ReadOnlyField(source='dept_manager.emp_name')

    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['dept_id',]

class UpdateDepartmentSerializer(serializers.ModelSerializer):
    dept_manager = serializers.PrimaryKeyRelatedField(
        queryset=EmpUser.objects.all(), allow_null=True, required=False
    )
    class Meta:
        model = Department
        fields = ['dept_name', 'dept_manager']