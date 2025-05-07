from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Department
from .serializers import DepartmentSerializer
from users.permissions import IsBoss,CanViewDepartmentUsers
from users.models import EmpUser

# Create your views here.
class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (CanViewDepartmentUsers,IsAuthenticated)

    def perform_create(self, serializer):
        user = self.request.user
        if user.emp_role!= 'boss':
            raise ValidationError("只有部门老板才能创建部门")
        manager = serializer.validated_data.get('dept_manager')
        # emp = EmpUser.objects.filter(department=serializer.instance, emp_role='manager').first()
        if manager and (manager.emp_role != 'manager' or manager.department != serializer.instance):
            raise ValidationError("部门经理必须是本部门的经理角色用户")
        serializer.save()


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsBoss,IsAuthenticated)

    def perform_update(self, serializer):
        manager = serializer.validated_data.get('dept_manager')
        print(manager.emp_role, manager.department, serializer.instance)
        if manager and (manager.emp_role != 'manager' or manager.department != serializer.instance):
            raise ValidationError("部门经理必须是本部门的经理角色用户")
        serializer.save()


