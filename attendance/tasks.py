from celery import shared_task
from .models import Attendance
from users.models import EmpUser
from datetime import datetime
@shared_task
def check_attendance():
    today = datetime.now().date()
    emps = EmpUser.objects.all()
    for emp in emps:
        att_id = f"{emp.emp_id}_{today.strftime('%Y%m%d')}"
        if not Attendance.objects.filter(attendance_id=att_id).exists():
            Attendance.objects.create(
                attendance_id=att_id,
                emp_user=emp,
                date=today,
                status='absent'
            )
