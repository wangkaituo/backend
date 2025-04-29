import django_filters
from.models import EmpUser

class EmpUserFilter(django_filters.FilterSet):
    emp_name = django_filters.CharFilter(field_name='emp_name', lookup_expr='icontains', required=False)
    emp_join_date_after = django_filters.DateFilter(field_name='emp_join_date', lookup_expr='gte', required=False)
    emp_join_date_before = django_filters.DateFilter(field_name='emp_join_date', lookup_expr='lte', required=False)

    class Meta:
        model = EmpUser
        fields = ['emp_name', 'emp_join_date_after', 'emp_join_date_before']  # 确保字段名称与前端一致
