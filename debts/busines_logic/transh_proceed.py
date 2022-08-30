"""Some logic to work with debts"""
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from debts.models import Person, Expense, Transh, Debt


def add_debt(transh, charge=None):
    """Will add new debt or update existing"""
    try:
        existing_debt = Debt.objects.get(creditor=transh.payer, debtor=transh.receiver)
        existing_debt.charge += transh.charge if not charge else Decimal(charge)
        existing_debt.save()
    except ObjectDoesNotExist:
        new_debt = Debt(
            creditor=transh.payer,
            debtor=transh.receiver,
            charge=transh.charge if not charge else Decimal(charge),
        )
        new_debt.save()
    return "Debt added"


def proceed_transh(transh):
    """Will check if transh covers debt. And close/prtly close the debt and create reverse debt if necessary"""
    try:
        debt = Debt.objects.get(creditor=transh.receiver, debtor=transh.payer)
        if debt.charge > transh.charge:
            debt.charge -= transh.charge
            debt.save()
        elif debt.charge < transh.charge:
            add_debt(transh, charge=transh.charge - debt.charge)
            debt.charge = 0
            debt.save()
        else:
            debt.charge = 0
            debt.save()
    except ObjectDoesNotExist:
        add_debt(transh)
