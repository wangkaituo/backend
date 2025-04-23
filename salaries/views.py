from rest_framework import generics
from.models import Salary
from.serializers import SalarySerializer
# Create your views here.
class SalaryList(generics.ListCreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer

class SalaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer