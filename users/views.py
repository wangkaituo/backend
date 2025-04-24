from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .serializers import EmpUserSerializer
from .models import EmpUser
from .permissions import IsSelfOrBoss, CanViewDepartmentUsers


# 修正导入语句，补充新增的权限类
class EmpUserList(generics.ListCreateAPIView):
    queryset = EmpUser.objects.all()
    serializer_class = EmpUserSerializer
    permission_classes = [IsAuthenticated, CanViewDepartmentUsers]

    def get_queryset(self):
        user = self.request.user
        if user.emp_role == 'boss':
            queryset = EmpUser.objects.all()
        elif user.emp_role == 'manager' and self.request.method in SAFE_METHODS:
            queryset = EmpUser.objects.filter(department=user.department)
        else:
            queryset = EmpUser.objects.none()
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        if user.emp_role == 'boss':
            department = data.get("department", None)
            if not department:  # 添加参数校验
                raise ValidationError("Department parameter is required for boss users")

            if EmpUser.objects.filter(department=department, emp_role='manager').exists():  # 改用exists()更高效
                raise ValidationError("You can only create one manager in each department.")
            serializer.save()  # 移出else块

        elif user.emp_role == 'manager':
            serializer.save(department=user.department, emp_role='employee')

        else:
            raise PermissionError('You do not have permission to perform this action.')


# 修正权限组合逻辑


class EmpUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmpUser.objects.all()
    serializer_class = EmpUserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrBoss]


    # 修正权限判断逻辑
    def perform_destroy(self, instance):
        user = self.request.user
        if user.emp_role == 'boss':
            instance.delete()
        else:
            raise PermissionError('You do not have permission to perform this action.')

