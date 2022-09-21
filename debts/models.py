"""Here will be models for debt app"""
from datetime import date
from django.db import models


class Person(models.Model):
    """A class for person who can bee a creditr or a debtor"""
    name = models.CharField(max_length=30, verbose_name="Имя", unique=True)
    name_in_dat = models.CharField(max_length=150, default='dat', verbose_name="Имя в дательном падеже")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"


class Expense(models.Model):
    """A class for expense model"""
    name = models.CharField(max_length=30, verbose_name="Имя", unique=True)
    comment = models.CharField(max_length=300, blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Основание"
        verbose_name_plural = "Основания"


class Transh(models.Model):
    """A model for single transh"""
    payer = models.ForeignKey(Person, related_name="payments", on_delete=models.CASCADE, verbose_name="Плательщик")
    receiver = models.ForeignKey(Person, related_name="receeves", on_delete=models.CASCADE, verbose_name="Получатель")
    expense = models.ForeignKey(Expense, related_name="transhes", on_delete=models.CASCADE, verbose_name="Основание")
    date = models.DateField(default=date.today, verbose_name="Дата")
    charge = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    return_required = models.BooleanField(default=True)

    def __str__(self):
        return f"Трашн от {self.payer} к {self.receiver} на сумму {self.charge}"

    class Meta:
        verbose_name = "Транш"
        verbose_name_plural = "Транши"


class Debt(models.Model):
    """A model to store a debt record"""
    creditor = models.ForeignKey(Person, related_name="credits", on_delete=models.CASCADE, verbose_name="Кредитор")
    debtor = models.ForeignKey(Person, related_name="debts", on_delete=models.CASCADE, verbose_name="Должник")
    charge = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")

    def __str__(self):
        return f"Долг от {self.debtor} к {self.creditor} на сумму {self.charge}"

    class Meta:
        verbose_name = "Долг"
        verbose_name_plural = "Долги"
