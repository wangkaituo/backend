from rest_framework import generics
from .models import Salary
from .serializers import SalarySerializer
from datetime import datetime
import calendar
from users.permissions import IsBoss
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from attendance.models import Attendance


# Create your views here.
class SalaryList(generics.ListCreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        emp = data.get('emp_user')
        now_year = datetime.now().year
        now_month = datetime.now().month
        _, days_in_month = calendar.monthrange(now_year, now_month)
        base_salary = data.get("basic_salary")
        base_salary = float(base_salary)
        if not base_salary:
            raise ValidationError({"error": "Base salary is required"})
        leave_days = Attendance.objects.filter(emp_user=emp, date__year=now_year, date__month=now_month,
                                               status='leave').count()
        decut_days = Attendance.objects.filter(emp_user=emp, date__year=now_year, date__month=now_month,
                                               status='absent').count()
        final_salary = float((1 - (leave_days + decut_days) / days_in_month) * base_salary)
        if Salary.objects.filter(emp_user=emp, year=now_year, month=now_month).exists():
            raise ValidationError({"error": "Salary already exists for this employee in this month"})
        else:
            serializer.save(year=now_year, month=now_month, final_salary=final_salary, leave_days=leave_days,
                            deduction_days=decut_days)
    def get_queryset(self):
        emp = self.request.user
        emp_role = emp.emp_role
        if emp_role == 'boss':
            return Salary.objects.all()
        else:
            return Salary.objects.filter(emp_user=emp)

class SalaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer

    def get_queryset(self):
        emp = self.request.user
        emp_role = emp.emp_role
        if emp_role == 'boss':
            return Salary.objects.all()
        else:
            return Salary.objects.filter(emp_user=emp)

    def perform_update(self, serializer):
        raise ValidationError({"error": "You are not allowed to update salary"})

    def perform_destroy(self, instance):
        raise ValidationError({"error": "You are not allowed to delete salary"})
