from django.urls import re_path

from.views import AttendanceList, AttendanceDetail

urlpatterns = [
    re_path(r'^attendance/$',AttendanceList.as_view(), name='attendance-list'),
    re_path(r'^attendance/(?P<pk>[0-9]+)/$',AttendanceDetail.as_view(), name='attendance-detail'),
]
