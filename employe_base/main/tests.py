from django.test import TestCase, Client
from django.urls import reverse

from .models import Employee, Department

class EmployeeModelTest(TestCase):
    
    def setUp(self):
        dep = Department.objects.create(
            name='разработка'
        )

        employee = Employee.objects.create(
            first_name='андрей',
            last_name='Петров',
            middle_name='евгеньевич',
            birthday='2000-01-01',
            email='a.petrov@test.ru',
            phone='+78142315478',
            start_date='2018-05-05',
            end_date=None,
            position='Программист',
            department=dep
            )
        return employee
    
    def test_employee_creation(self):
        a = self.setUp()
        self.assertTrue(isinstance(a, Employee))

class ViewsAceessTest(TestCase):
    client = Client()

    def test_employee_list(self):
        response = self.client.get('')
        self.assertIs(response.status_code, 200)

    def test_employee_detail(self):
        a = EmployeeModelTest.setUp(self)

        response = self.client.get('/employee/1')
        self.assertIs(response.status_code, 200)

        response = self.client.get('/employee/2')
        self.assertEqual(response.status_code, 404)

    def test_alpabetic_list(self):
        response = self.client.get('/alphabetic')
        self.assertIs(response.status_code, 200)

        response = self.client.get('/alphabetic?letters=all')
        self.assertIs(response.status_code, 200)

class QueryViewTests(TestCase):
    pass 