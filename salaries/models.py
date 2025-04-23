from django.db import models


# Create your models here.
class Salary(models.Model):
    salary_id = models.AutoField(primary_key=True, verbose_name='薪资编号')
    emp_user = models.ForeignKey('users.EmpUser', on_delete=models.CASCADE, db_column='emp_user_id',
                                 verbose_name='员工编号')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='基本工资')
    final_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='最终工资')
    deduction_days = models.IntegerField(verbose_name='扣除天数')
    leave_days = models.IntegerField(verbose_name='请假天数')
    year = models.IntegerField(null=False, verbose_name='年份')
    month = models.IntegerField(null=False, verbose_name='月份')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.salary_id

    class Meta:
        ordering = ['-created_at']
        verbose_name = '薪资信息'
        verbose_name_plural = '薪资信息'
