"""A logic to create a form of report on debts"""
from debts.models import Person


def form_report(report):
    """Will give a form to pyment_order_report"""
    output = ""
    if len(report) == 0:
        output += '<div class="alert alert-success" role="alert">Все долги погашены</div>'
        return output
    for debtor in report:
        output += f"<p class='my-3'><strong>{debtor}:</strong><br>"
        for creditor, charge in report[debtor].items():
            cred_name = Person.objects.get(name=creditor)
            output += f"<span>{cred_name.name_in_dat} - {charge}</span><br>"
        output += "</p>"
    return output
