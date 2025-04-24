from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .models import Department
from .serializers import DepartmentSerializer
from users.permissions import IsBoss
from users.models import EmpUser

# Create your views here.
class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsBoss,)

    def perform_create(self, serializer):
        manager = serializer.validated_data.get('dept_manager')
        emp = EmpUser.objects.filter(department=serializer.instance, emp_role='manager').first()
        if manager and (manager.emp_role != 'manager' or manager.department != serializer.instance):
            raise ValidationError("部门经理必须是本部门的经理角色用户")
        serializer.save(dept_manager=emp.emp_id)


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsBoss,)

    def perform_update(self, serializer):
        manager = serializer.validated_data.get('dept_manager')
        if manager and (manager.emp_role != 'manager' or manager.department != serializer.instance):
            raise ValidationError("部门经理必须是本部门的经理角色用户")
        serializer.save()
