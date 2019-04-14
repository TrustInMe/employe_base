from django.contrib import admin
from .models import Department, Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'middle_name',
        'email',
        'phone',
        'position',
        'department',
    )
    list_filter = (
        'position',
        'department',
        'start_date',
        'end_date',
    )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )