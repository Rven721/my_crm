'''Set of forms for contract app'''
from django.db import models
from crm.models import Project


class Agent(models.Model):
    '''Form to describe agent'''
    name = models.CharField(max_length=100, verbose_name='Наименование', unique=True)
    data = models.TextField(verbose_name='Свдения о контрагенте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'


class Terms(models.Model):
    '''Form for describtion of contract terms'''
    name = models.CharField(max_length=100, verbose_name='Наименование', unique=True)
    first_pay = models.FloatField(verbose_name='Первый платеж')
    second_pay = models.FloatField(verbose_name='Второй платеж')
    success_fee = models.FloatField(verbose_name='Плата за успех')
    success_fee_base = models.CharField(max_length=10, verbose_name='База для расчета', choices=[('grant', 'Грант'), ('project', 'Проект')])
    team_fee = models.FloatField(verbose_name='Выручка команды')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Условия'
        verbose_name_plural = 'Условия'


class Contract(models.Model):
    '''From to describe a contract'''

    PAYMENT_STATUS_CHOICES = [
        ('first_pay_wait', 'Платеж 1 ожидание'),
        ('first_pay_receive', 'Платеж 1 получен'),
        ('second_pay_wait', 'Платеж 2 ожидание'),
        ('second_pay_receive', 'Платеж 2 получен'),
        ('success_fee_wait', 'Финальный платеж ожидание'),
        ('success_fee_receive', 'Финальный платеж получен'),
        ('special_terms', 'Особые условия'),
    ]

    number = models.CharField(max_length=20, verbose_name='Номер', unique=True)
    date = models.DateField(verbose_name='Дата')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, verbose_name='Агент')
    terms = models.ForeignKey(Terms, on_delete=models.CASCADE, verbose_name='Условия')
    payment_status = models.CharField(max_length=25, verbose_name='Статус оплаты', default='first_pay', choices=PAYMENT_STATUS_CHOICES)
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'Контракт по проекту {self.project}'

    @property
    def get_revenue_fix_pt1(self):
        '''Wll return first fix part of fee on contract'''
        return self.terms.first_pay

    @property
    def get_revenue_fix_pt2(self):
        '''Wll return second fix part of fee on contract'''
        return self.terms.second_pay

    @property
    def get_revenue_fix(self):
        '''Wll return fix part of fee on contract'''
        rev = self.terms.first_pay + self.terms.second_pay
        return rev

    @property
    def get_success_fee(self):
        '''Wll return success fee acording to the terms of the contract'''
        if self.terms.success_fee_base == 'grant':
            fee = self.project.grant * self.terms.success_fee
        else:
            fee = self.project.full_cost * self.terms.success_fee
        return fee

    @property
    def get_team_revenue(self):
        '''Wll return team fee acording to the terms of the contract'''
        fix_fee = self.get_revenue_fix
        success_fee = self.get_success_fee
        team_fee = (fix_fee + success_fee) * self.terms.team_fee
        return team_fee

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'


class StatusChangeLog(models.Model):
    '''Model will store log of files status changes'''
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Проект')
    date = models.DateField(auto_now_add=True, verbose_name='дата')
    status = models.CharField(max_length=50, verbose_name='status')

    def __str__(self):
        return f'{self.contract} {self.status} {self.date}'

    class Meta:
        verbose_name = 'Смена статусов'
        verbose_name_plural = 'Смены статусов'
