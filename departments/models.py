from django.db import models


# Create your models here.
class Department(models.Model):
    dept_id = models.CharField(max_length=10, primary_key=True, unique=True, verbose_name='部门ID')
    dept_name = models.CharField(max_length=50, unique=True, verbose_name='部门名称')
    dept_manager = models.ForeignKey('users.EmpUser', limit_choices_to={'emp_role': 'manager'},
                                        related_name='dept_manager',null=True, blank=True ,on_delete=models.SET_NULL, verbose_name='部门经理')

    def __str__(self):
        return self.dept_name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.dept_id:
            last = Department.objects.all().order_by('dept_id').last()
            last_id = int(last.dept_id)
            new_id = f"{last_id+1:03d}"
            self.dept_id = new_id
            super().save(*args, **kwargs)
