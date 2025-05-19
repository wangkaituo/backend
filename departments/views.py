from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Department
from .serializers import DepartmentSerializer, UpdateDepartmentSerializer
from users.permissions import IsBoss, CanViewDepartmentUsers
from users.models import EmpUser
from .change_dept import change_dept

# Create your views here.
class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (CanViewDepartmentUsers, IsAuthenticated)

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        dept_manager = data.get('dept_manager')
        print(dept_manager)
        print(data)
        if user.emp_role != 'boss':
            raise ValidationError({"error": "Only Boss can create department"})
        manager = serializer.validated_data.get('dept_manager')
        # emp = EmpUser.objects.filter(department=serializer.instance, emp_role='manager').first()
        if manager and (manager.emp_role != 'manager' or manager.department != serializer.instance):
            raise ValidationError({"error": "Department Manager must be a manager of the department"})
        serializer.save()


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    permission_classes = (IsBoss, IsAuthenticated)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateDepartmentSerializer
        return DepartmentSerializer

    def perform_update(self, serializer):
        dept = self.get_object()
        print(dept, type(dept))
        data = self.request.data
        dept_manager = data.get('dept_manager')
        dept_name = data.get('dept_name')
        print(dept_manager, type(dept_manager))
        print(dept_name, type(dept_name))
        old_manager = dept.dept_manager
        print(old_manager, type(old_manager))
        # role = EmpUser.objects.filter(emp_id=dept_manager).first().emp_role
        # if role =='manager':
        #     Department.objects.get(dept_manager=dept_manager).save(dept_manager=None)

        if dept_manager:
            manager = EmpUser.objects.filter(emp_id=dept_manager).first()
            if manager.emp_role == 'manager':
                old_dept = Department.objects.get(dept_manager=manager).dept_id
                print(old_dept, type(old_dept))
                change_dept(old_dept)
            else:
                manager.emp_role = 'manager'
            manager.department = dept
            print(manager, type(manager))
            manager.save()
            Department.objects.filter(dept_id=dept.dept_id).update(dept_manager=manager, dept_name=dept_name)

        if old_manager and old_manager.emp_id != dept_manager:
            old_manager.emp_role = 'employee'
            old_manager.save()
        serializer.save()
