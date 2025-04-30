from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('normal', '正常打卡'),
        ('leave', '请假'),
        ('absent', '缺勤'),
        ('late', '迟到'),
    )
    attendance_id = models.CharField(primary_key=True,max_length=100, unique=True ,verbose_name='考勤编号')
    emp_user = models.ForeignKey('users.EmpUser', on_delete=models.CASCADE, null=True, db_column='emp_user_id',
                                 related_name='user_attendance',
                                 verbose_name='员工号')
    date = models.DateField(auto_now_add=True, verbose_name='日期')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='状态')

    def __str__(self):
        return str(self.attendance_id)

    class Meta:
        verbose_name = '考勤信息'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        # 在保存之前生成考勤编号
        self.attendance_id = f"{self.emp_user.emp_id}_{self.date}"
        super(Attendance, self).save(*args, **kwargs)
        # 这里调用父类的 save 方法，确保数据被保存到数据库中




