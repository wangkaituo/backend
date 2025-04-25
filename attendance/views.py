from rest_framework import generics
from .models import Attendance
from .serializers import AttendanceSerializer
from datetime import date
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from users.models import EmpUser

class AttendanceList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        now_time = date.today()
        now_time = str(now_time).replace('-', '')
        emp_id = self.request.user.emp_id
        att_id = f"{emp_id}_{now_time}"
        if Attendance.objects.filter(attendance_id=att_id).exists():
            raise ValidationError({"error": "Attendance already taken for today"})

        else:
            serializer.save(emp_user_id=emp_id, date=now_time)

    def get_queryset(self):
        emp_role = self.request.user.emp_role
        if emp_role == 'boss':
            return Attendance.objects.all()
        elif emp_role == 'manager':
            department = self.request.user.department
            emp_ids = EmpUser.objects.filter(department=department).values_list('emp_id', flat=True)
            return Attendance.objects.filter(emp_user_id__in=emp_ids)
        else:
            emp_id = self.request.user.emp_id
            return Attendance.objects.filter(emp_user_id=emp_id)

class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
# Create your views here.

    def get_queryset(self):
        emp_role = self.request.user.emp_role
        if emp_role == 'boss':
            return Attendance.objects.all()
        elif emp_role == 'manager':
            department = self.request.user.department
            emp_ids = EmpUser.objects.filter(department=department).values_list('emp_id', flat=True)
            return Attendance.objects.filter(emp_user_id__in=emp_ids)
        else:
            emp_id = self.request.user.emp_id
            return Attendance.objects.filter(emp_user_id=emp_id)
    #禁止删除
    def perform_destroy(self, instance):
        raise ValidationError({"error": "Attendance can not be deleted"})
    #禁止修改
    def perform_update(self, serializer):
        raise ValidationError({"error": "Attendance can not be updated"})