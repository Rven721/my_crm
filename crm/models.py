from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class ProjectDeliver(models.Model):
    name = models.CharField(max_length=55)
    slug = models.SlugField(max_length=55, default='user')
    conditions_of_work = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Источник проекта'
        verbose_name_plural = 'Источники проекта'


class Contact(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    second_name = models.CharField(max_length=50, verbose_name='Отчество', blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=True, null=True)
    email = models.EmailField(max_length=124, verbose_name='e-mail', blank=True, null=True)
    phone = models.CharField(max_length=12, verbose_name='Телефон', blank=True, null=True)
    additional_info = models.TextField(blank=True, verbose_name='Дополнительная информация')

    def __str__(self):
        if self.last_name:
            full_name = str(self.first_name) + ' ' + str(self.last_name)
        else:
            full_name = str(self.first_name)
        return full_name

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Company(models.Model):
    inn_number = models.CharField(max_length=10, verbose_name='ИНН', unique=True)
    ogrn_number = models.CharField(max_length=13, verbose_name='ОГРН', unique=True)
    short_name = models.CharField(max_length=250, verbose_name='Сокращенное наименование')
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    contacts = models.ManyToManyField(Contact, verbose_name='Контакты', related_name='companies', blank=True)

    def __str__(self):
        return f'{self.short_name}'

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Project(models.Model):
    name = models.CharField(max_length=500, unique=True, verbose_name='Короткое название проекта')
    full_name = models.CharField(max_length=500, unique=True, blank=True, verbose_name='Полное название проекта')
    description = models.TextField(null=True, verbose_name='Описание')
    start_date = models.DateField(null=True, verbose_name='Начало проекта')
    end_date = models.DateField(null=True, verbose_name='Окончание проекта')
    grant = models.FloatField(null=True, verbose_name='Грант')
    full_cost = models.FloatField(null=True, verbose_name='Бюджет проекта')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, related_name='projects', verbose_name='Компания')
    contacts = models.ManyToManyField(Contact, related_name='projects', verbose_name='Контакты', blank=True)
    project_deliver = models.ForeignKey(ProjectDeliver, related_name='projects', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Источник проекта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Status(models.Model):
    status_list = [
        ('new', 'Новый проект'),
        ('progress', 'В работе'),
        ('finished', 'Работа завершена'),
    ]

    status = models.CharField(max_length=10, choices=status_list, verbose_name='Статус')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='statuses', verbose_name='Проект')

    def __str__(self):
        return f"{self.status}-{self.project}"

    class Meta:
        verbose_name = 'Статус проекта'
        verbose_name_plural = 'Статусы проектов'


class Event(models.Model):
    """Описание сущности событие, которое может произойти с проектом"""
    category_list = [
        ('text_consult', 'Письменная консультация'),
        ('phone_consult', 'Телефонная консультация'),
        ('call', 'ВКС'),
        ('document_transfer', 'Обмен документами'),
        ('paper_check', 'Работа с документами'),
        ('data_request', 'Запрос информации'),
        ('project_update', 'Изменение статуса'),
        ('discuss', 'Обсуждение'),
        ('due_dil', 'Контрактация'),
    ]
    projects = models.ManyToManyField(Project, related_name='events', verbose_name='Проекты')
    category = models.CharField(max_length=25, choices=category_list, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(blank=True, null=True, default=timezone.now, verbose_name='Дата')
    time = models.TimeField(blank=True, null=True, default=timezone.now, verbose_name='Время')
    invited_persons = models.ManyToManyField(User, blank=True, verbose_name='Приглашенные сотрудники')
    took_time = models.IntegerField(blank=True, null=True, verbose_name='Затраченное время в секундах')
    result = models.TextField(blank=True, null=True, verbose_name='Результат')
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='events',
        verbose_name='Автор события',
    )
    small = models.BooleanField(default=False, verbose_name='Добавить в календарь')

    def __str__(self):
        return f'{self.get_category_display()}, {self.date}'

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def get_absolute_url(self):
        day = self.date.day
        month = self.date.month
        year = self.date.year
        return reverse('events_on_date', kwargs={
            'day': day,
            'month': month,
            'year': year,
        })


class Task(models.Model):
    """Description of task for event"""
    name = models.CharField(max_length=120, verbose_name='Название задачи')
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Дата начала')
    end_date = models.DateTimeField(default=timezone.now, verbose_name='Дата окончания')
    doer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks", blank=True, null=True, verbose_name='Исполнители')
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name="tasks", blank=True, null=True, verbose_name='События')
    description = models.TextField(blank=True, verbose_name='Описание задачи')

    def __str__(self):
        return f"{self.name}-{self.event} "

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskStatus(models.Model):
    """A class to track task status changes"""
    STATUS_LIST = [
        ("NEW", "Новая задача"),
        ("PROGRESS", "В работе"),
        ("DONE", "Завершено"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_LIST, verbose_name='Статус')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='statuses', verbose_name='Задача')

    def __str__(self):
        return f"{self.status}-{self.task}"

    class Meta:
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задачи'


class Document(models.Model):
    name = models.CharField(max_length=120, verbose_name='Название документа')
    pages = models.IntegerField(default=1, verbose_name='Число страниц')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='documents', verbose_name='Событие')

    def __str__(self):
        return self.name
