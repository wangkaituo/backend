from rest_framework import serializers
from users.models import EmpUser
from.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    dept_manager_name = serializers.ReadOnlyField(source='dept_manager.emp_name')


    class Meta:
        model = Department
        fields = '__all__'