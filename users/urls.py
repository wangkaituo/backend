from django.urls import path, re_path

from .views import EmpUserList, EmpUserDetail

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    re_path(r'^emp_users/$', EmpUserList.as_view(), name='users'),
    re_path(r'^emp_users/(?P<pk>[0-9]+)/$', EmpUserDetail.as_view(), name='user-detail'),

    # path('emp_users/', EmpUserView.as_view(), name='users')
]
urlpatterns = format_suffix_patterns(urlpatterns)

