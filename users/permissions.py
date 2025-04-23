from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelfOrBoss(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        # 员工可以查看自己的信息和修改自己的信息
        if obj == user:
            return True
        # 老板可以查看所有员工信息，修改员工信息
        if user.emp_role == 'boss':
            return True
        # 经理可以查看自己信息，修改自己信息
        if user.emp_role == 'manager' and request.method in SAFE_METHODS:
            return obj == user
        return False


class CanViewDepartmentUsers(BasePermission):
    """
    老板可以查看所有员工，部门主管只能查看本部门员工
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.emp_role in ['boss', 'manager']
