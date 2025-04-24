from rest_framework import serializers
from users.models import EmpUser
from.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    dept_manager_name = serializers.ReadOnlyField(source='dept_manager.emp_name')
    
    def validate_dept_manager(self, value):
        if value:
            if value.emp_role != 'manager':
                raise serializers.ValidationError("该员工不是经理角色")
            if value.department != self.instance:
                raise serializers.ValidationError("该经理不属于当前部门")
        return value

    class Meta:
        model = Department
        fields = '__all__'