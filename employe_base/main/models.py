from django.db import models
from phone_field import PhoneField

class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='Отдел')

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
    
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """ Капитализируем """
        val = getattr(self, 'name', False)
        if val:
            setattr(self, 'name', val.capitalize())
        super(Department, self).save(*args, **kwargs)


class Employee(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=200, verbose_name='Отчество')
    birthday = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(max_length=100, verbose_name='E-mail')
    phone = PhoneField()
    start_date = models.DateField(verbose_name='Дата начала работы')
    end_date = models.DateField(verbose_name='Дата окончания работы', blank=True, null=True)
    position = models.CharField(max_length=200, verbose_name='Должность')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отдел')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
    
    def __str__(self):
        return str(self.last_name)

    def save(self, *args, **kwargs):
        """ ФИО с большой капитализируем """

        for field_name in ['first_name', 'last_name', 'middle_name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Employee, self).save(*args, **kwargs)