import django_filters
from .models import Attendance

class AttendanceFilter(django_filters.FilterSet):
    emp_name = django_filters.CharFilter(field_name='emp_user__emp_name', lookup_expr='icontains', required=False)  # 确保路径正确
    department = django_filters.CharFilter(field_name='emp_user__department__dept_name', lookup_expr='icontains', required=False)  # 确保路径正确
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact', required=False)  # 日期字段无需修改

    class Meta:
        model = Attendance
        fields = ['emp_name', 'department', 'date']