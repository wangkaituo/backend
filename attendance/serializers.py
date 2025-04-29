from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    emp_name = serializers.ReadOnlyField(source='emp_user.emp_name')
    cn_status = serializers.ReadOnlyField(source='get_status_display') 
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)  # 格式化创建时间
    department = serializers.CharField(source='emp_user.department.dept_name', read_only=True)  # 修改为返回部门名称
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('attendance_id', 'emp_user', 'date', 'create_time',)
