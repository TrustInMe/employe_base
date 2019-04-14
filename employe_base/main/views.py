from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView

from .models import Employee, Department

class EmployeesList(ListView):
    """ Главная страница. Страница списка сотрудников с
        фильтрами по отделу и текущему статусу работы в компании """

    template_name = 'employeeslist.html'
    paginate_by = 10

    def get_context_data(self):
        """ Выводим в контекст паггинацию +
            Выводим в контекст все отделы для опций фильтра """

        context = super().get_context_data()
        queryset = Employee.objects.all()

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            employees_page = paginator.page(page)
        except PageNotAnInteger:
            employees_page = paginator.page(1)
        except EmptyPage:
            employees_page = paginator.page(paginator.num_pages)

        departments = Department.objects.all().values_list('name', flat=True)

        context['departments'] = departments
        context['page'] = employees_page

        return context

    def get_queryset(self):
        """ Запрос данных, основанный на get запросе фильтра """

        queryset = Employee.objects.all()

        query_workers = self.request.GET.get('workers')
        query_department = self.request.GET.get('departments')

        if query_workers and query_department:
            if query_workers == 'current':
                queryset = Employee.objects.filter(
                    end_date__isnull=True,
                    department__name=query_department
                )
            elif query_workers == 'left':
                queryset = Employee.objects.filter(
                    end_date__isnull=False,
                    department__name=query_department
                )

        elif query_workers or query_department:
            if query_workers:
                if query_workers == 'current':
                    queryset = Employee.objects.filter(
                        end_date__isnull=True
                    )
                elif query_workers == 'left':
                    queryset = Employee.objects.filter(
                        end_date__isnull=False
                    )
            elif query_department:
                queryset = Employee.objects.filter(
                    department__name=query_department
                )

        return queryset


class EmployeeDetail(DetailView):
    """ Страница деталей по каждому сотруднику """

    queryset = Employee.objects.all()
    template_name = 'employeedetail.html'

    def get_object(self):
        obj = super(EmployeeDetail, self).get_object()
        return obj

class EmployeesListAlphabet(ListView):
    """ Страница списка сотрудников с фильтром по алфавитному указателю """

    template_name = 'alpabetic.html'

    def get_queryset(self):
        queryset = Employee.objects.all().order_by('last_name')

        query = self.request.GET.get('letters')

        if query:
            if query == 'А-Е':
                queryset = Employee.objects.filter(
                    Q(last_name__startswith='А') |
                    Q(last_name__startswith='Б') |
                    Q(last_name__startswith='В') |
                    Q(last_name__startswith='Г') |
                    Q(last_name__startswith='Д') |
                    Q(last_name__startswith='Е') |
                    Q(last_name__startswith='Ё')
                    ).order_by('last_name')

            elif query == 'Ж-М':
                queryset = Employee.objects.filter(
                    Q(last_name__startswith='Ж') |
                    Q(last_name__startswith='З') |
                    Q(last_name__startswith='И') |
                    Q(last_name__startswith='Й') |
                    Q(last_name__startswith='К') |
                    Q(last_name__startswith='Л') |
                    Q(last_name__startswith='М')
                    ).order_by('last_name')

            elif query == 'Н-Т':
                queryset = Employee.objects.filter(
                    Q(last_name__startswith='Н') |
                    Q(last_name__startswith='О') |
                    Q(last_name__startswith='П') |
                    Q(last_name__startswith='Р') |
                    Q(last_name__startswith='С') |
                    Q(last_name__startswith='Т')
                    ).order_by('last_name')

            elif query == 'У-Ш':
                queryset = Employee.objects.filter(
                    Q(last_name__startswith='У') |
                    Q(last_name__startswith='Ф') |
                    Q(last_name__startswith='Х') |
                    Q(last_name__startswith='Ц') |
                    Q(last_name__startswith='Ч') |
                    Q(last_name__startswith='Ш')
                    ).order_by('last_name')

            elif query == 'Щ-Я':
                queryset = Employee.objects.filter(
                    Q(last_name__startswith='Щ') |
                    Q(last_name__startswith='Ы') |
                    Q(last_name__startswith='Э') |
                    Q(last_name__startswith='Ю') |
                    Q(last_name__startswith='Я')
                    ).order_by('last_name')

        return queryset
