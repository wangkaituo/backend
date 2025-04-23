from django.db import models
# Create your models here.
class Department(models.Model):
    dept_id = models.CharField(max_length=10, primary_key=True,unique=True, verbose_name='部门ID')
    dept_name = models.CharField(max_length=50, unique=True, verbose_name='部门名称')

    def __str__(self):
        return self.dept_name
    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name



