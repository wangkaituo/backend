from django.db import models


# Create your models here.
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('normal', '正常打卡'),
        ('leave', '请假'),
        ('absent', '缺勤'),
    )
    attendance_id = models.AutoField(primary_key=True, verbose_name='考勤编号')
    emp_user = models.ForeignKey('users.EmpUser', on_delete=models.CASCADE, null=True, db_column='emp_user_id',
                                 related_name='user_attendance',
                                 verbose_name='员工号')
    date = models.DateField(auto_now_add=True, verbose_name='日期')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='状态')

    def __str__(self):
        return str(self.attendance_id)

    class Meta:
        verbose_name = '考勤信息'
        verbose_name_plural = verbose_name
