from rest_framework import generics
from .models import Salary
from .serializers import SalarySerializer
from datetime import datetime
from users.permissions import IsBoss
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
# Create your views here.
class SalaryList(generics.ListCreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsBoss,IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        emp = data.get('emp_user')
        now_year = datetime.now().year
        now_month = datetime.now().month
        print(now_year)
        print(now_month)
        print(data.get('emp_user'))
        if Salary.objects.filter(emp_user=emp, year=now_year, month=now_month).exists():
            raise ValidationError({"error": "Salary already exists for this employee in this month"})
        else:
            serializer.save(year=now_year, month=now_month)

class SalaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
