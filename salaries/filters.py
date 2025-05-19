import django_filters
from.models import Salary

class SalaryFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year', lookup_expr='exact')
    month = django_filters.NumberFilter(field_name='month', lookup_expr='exact')
    emp_name = django_filters.CharFilter(field_name='emp_user__emp_name', lookup_expr='icontains')
    department = django_filters.CharFilter(field_name='emp_user__department__dept_name', lookup_expr='icontains')

    class Meta:
        model = Salary
        fields = ['year','month', 'emp_name', 'department']

