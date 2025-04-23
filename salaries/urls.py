from django.urls import re_path

from.views import SalaryList,SalaryDetail

urlpatterns = [
    re_path(r'^salaries/$', SalaryList.as_view(), name='salaries'),
    re_path(r'^salaries/(?P<pk>\d+)/$', SalaryDetail.as_view(), name='salary-detail'),
]