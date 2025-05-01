from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# 用户管理器（必须配合 AbstractBaseUser 使用）
class EmpUserManager(BaseUserManager):
    def create_user(self, emp_id, emp_password=None, **extra_fields):
        if not emp_id:
            raise ValueError("员工 ID 必填")
        user = self.model(emp_id=emp_id, **extra_fields)
        user.set_password(emp_password)  # 使用哈希加密
        user.save(using=self._db)
        return user

    def create_superuser(self, emp_id, emp_password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(emp_id, emp_password, **extra_fields)


class EmpUser(AbstractBaseUser, PermissionsMixin):
    EMP_ROLE_CHOICES = (
        ('boss', 'Boss'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )

    emp_id = models.CharField(primary_key=True, max_length=6, unique=True, verbose_name='员工编号')
    emp_name = models.CharField(max_length=15, verbose_name='员工姓名')
    emp_email = models.EmailField(max_length=50, null=True, verbose_name='员工邮箱')
    emp_phone = models.CharField(max_length=11, unique=True, null=True, verbose_name='员工手机号')
    emp_role = models.CharField(max_length=10, choices=EMP_ROLE_CHOICES ,default='employee', verbose_name='员工角色')
    emp_join_date = models.DateField(auto_now_add=True, verbose_name='员工入职日期')

    department = models.ForeignKey(
        to='departments.Department',
        db_column='department_id',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='所属部门号'
    )
    
    # 额外认证字段必须加
    is_active = models.BooleanField(default=True)  # 确保该字段生效
    
    def is_active(self):
        return self.is_active  # 需要实现该方法
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'emp_id'  # 用作登录的字段
    REQUIRED_FIELDS = ['emp_name']  # 创建 superuser 时需要输入的字段

    objects = EmpUserManager()

    class Meta:
        db_table = 'users_empuser'
        verbose_name = '员工信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.emp_name

    def save(self, *args, **kwargs):
        if not self.emp_id:
            last = EmpUser.objects.filter(emp_id__startswith='22').order_by('-emp_id').first()
            if last:
                last_num = int(last.emp_id[2:])
                next_id = f"22{last_num + 1:03d}"
            else:
                next_id = "22001"
            self.emp_id = next_id
        super().save(*args, **kwargs)