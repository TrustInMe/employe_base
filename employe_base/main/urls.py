from django.urls import path

from .views import EmployeesList, EmployeeDetail, EmployeesListAlphabet

app_name = 'main'

urlpatterns = [
    path('', EmployeesList.as_view(), name='employeeslist'),
    path('alphabetic', EmployeesListAlphabet.as_view(), name='alphabetic'),
    path('employee/<pk>', EmployeeDetail.as_view(), name='employeedetail'),

]