from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    # dept_manager = serializers.CharField(source='dept_manager.emp_name')
    dept_manager_name = serializers.ReadOnlyField(source='dept_manager.emp_name')
    class Meta:
        model = Department
        fields = '__all__'

    # def validate(self, data):
    #     if data['dept_manager'] is None:
    #         raise ValidationError("Department manager is required.")
    #     return data