from rest_framework import serializers
from.models import Salary

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ['salary_id','basic_salary','final_salary','emp_user']