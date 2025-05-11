from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .serializers import EmpUserSerializer, ChangeEmpUserSerializer, ChangeSelf
from .models import EmpUser
from .permissions import IsSelfOrBoss, CanViewDepartmentUsers
from paginations.emp_pagination import EmpPagination
from .filters import EmpUserFilter
from rest_framework import filters
import django_filters


# 修正导入语句，补充新增的权限类


class EmpUserList(generics.ListCreateAPIView):
    queryset = EmpUser.objects.all()
    serializer_class = EmpUserSerializer
    permission_classes = [IsAuthenticated, CanViewDepartmentUsers]
    pagination_class = EmpPagination
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = EmpUserFilter  # 修正为 filterset_class

    # filterset_fields = ['emp_name', 'emp_join_date']

    def get_queryset(self):
        user = self.request.user
        if user.emp_role == 'boss':
            queryset = EmpUser.objects.filter(emp_role__in=['employee', 'manager'])  # 添加排序字段
        elif user.emp_role == 'manager' and self.request.method in SAFE_METHODS:
            queryset = EmpUser.objects.filter(department=user.department)
        else:
            queryset = EmpUser.objects.none()
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        emp_role = data.get("emp_role", None)
        if user.emp_role == 'boss':
            department = data.get("department", None)
            if not department:  # 添加参数校验
                raise ValidationError({"error": "Department parameter is required for boss users"})
            # 改用exists()更高效
            if emp_role == 'manager' and EmpUser.objects.filter(department=department, emp_role='manager').exists():
                raise ValidationError({"error": "You can only create one manager in each department."})
            serializer.save()  # 移出else块
        elif user.emp_role == 'manager':
            serializer.save(department=user.department, emp_role='employee')
        else:
            raise PermissionError({"error": "You do not have permission to perform this action."})


class EmpUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmpUser.objects.all()
    permission_classes = [IsAuthenticated, IsSelfOrBoss]

    # 修正权限判断逻辑
    def perform_destroy(self, instance):
        user = self.request.user
        if user.emp_role == 'boss':
            instance.delete()
        else:
            raise PermissionError('You do not have permission to perform this action.')

    def get_queryset(self):
        user = self.request.user
        if user.emp_role == 'boss':
            queryset = EmpUser.objects.all()  # 添加排序字段
        elif user.emp_role == 'manager' and self.request.method in SAFE_METHODS:
            queryset = EmpUser.objects.filter(department=user.department).order_by('emp_id')
        else:
            queryset = EmpUser.objects.filter(emp_id=user.emp_id)
        return queryset

    def get_serializer_class(self):
        user = self.request.user
        emp_id = self.kwargs.get("pk")  # 从 URL 参数中获取 emp_id
        emp_role = user.emp_role  # 如果需要，可以从请求体中获取其他字段
        # print(emp_role)调试日志
        # print(emp_id,type(emp_id))
        # print(user.emp_id,type(user.emp_id))
        if self.request.method in ['PUT', 'PATCH'] and emp_id == user.emp_id:
            return ChangeSelf  # 使用专门的序列化器
        if self.request.method in ['PUT', 'PATCH'] and emp_role == 'boss' and emp_id != user.emp_id:
            return ChangeEmpUserSerializer
        return EmpUserSerializer

    def perform_update(self, serializer):
        user = self.request.user
        emp_id = self.kwargs.get("pk")  # 从 URL 参数中获取 emp_id
        emp_role = user.emp_role  # 如果需要，可以从请求体中获取其他字段
        department = self.request.data.get("department", None)  # 校验部门参数
        # print(emp_role)#调试日志
        # print(department)
        # print(EmpUser.objects.filter(department=department, emp_role='manager').exists() and self.request.data.get("emp_role", None) == 'manager')
        if emp_id == user.emp_id:
            # print(serializer)#调试日志
            serializer.save()
        elif emp_role == 'boss' and emp_id != user.emp_id:
            if EmpUser.objects.filter(department=department, emp_role='manager').exists() and self.request.data.get("emp_role", None) == 'manager':
                raise ValidationError({"error": "You can only create one manager in each department."})
            serializer.save()
        else:
            raise PermissionError({"error": "You do not have permission to perform this action."})