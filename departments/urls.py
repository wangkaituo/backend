from django.urls import re_path

from .views import DepartmentDetail,DepartmentList
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    re_path(r'^departments/$', DepartmentList.as_view(), name='department-list'),
    re_path(r'^departments/(?P<pk>\d+)/$', DepartmentDetail.as_view(), name='department-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
