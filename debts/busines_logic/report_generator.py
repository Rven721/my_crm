"""A logic to create a form of report on debts"""
from debts.models import Person
from .thousand_separator import get_nubmer_with_serparaes


def form_report(report):
    """Will give a form to pyment_order_report"""
    output = "<div class='container w-80 d-inline-flex justify-content-evenly'>"
    if len(report) == 0:
        output += '<div class="alert alert-success" role="alert">Все долги погашены</div>'
        return output
    for debtor in report:
        output += f"<p class='m-3'><strong>{debtor}:</strong><br>"
        for creditor, charge in report[debtor].items():
            creditor = Person.objects.get(name=creditor)
            debtor = Person.objects.get(name=debtor)
            close_link = f"<a href='/debts/transh/add/?cred={creditor.id}&deb={debtor.id}&charge={round(charge,2)}'><i class='ms-2 bi bi-check-square text-success'></i></a>"
            output += f"<span class='my-3'>{creditor.name_in_dat} - {get_nubmer_with_serparaes(charge)}</span>{close_link}<br>"
        output += "</p>"
    output += "</div>"
    return output
