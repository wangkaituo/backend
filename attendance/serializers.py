from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    emp_name = serializers.ReadOnlyField(source='emp_user.emp_name')
    cn_status = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Attendance
        fields = '__all__'

