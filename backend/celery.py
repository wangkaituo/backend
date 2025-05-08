import os
from celery import Celery
from django.conf import settings
#设置系统环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')
#加载celery配置
app.config_from_object('django.conf:settings', namespace='CELERY')
#自动发现任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)