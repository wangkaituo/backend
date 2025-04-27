from rest_framework import serializers
from .models import Salary

class SalarySerializer(serializers.ModelSerializer):
    emp_name = serializers.ReadOnlyField(source='emp_user.emp_name')
    create_date = serializers.DateTimeField(source='created_at', format='%Y-%m-%d')  # 新增日期格式化字段
    department_name = serializers.ReadOnlyField(source='emp_user.department.dept_name')  # 修正外键路径
    
    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = [
            'year', 'month', 
            'final_salary', 'leave_days',
            'deduction_days', 'created_at'  # 新增原始日期字段保护
        ]