"""A logic to create a form of report on debts"""


def form_report(report):
    """Will give a form to pyment_order_report"""
    output = ""
    if len(report) == 0:
        output += '<div class="alert alert-success" role="alert">Все долги погашены</div>'
        return output
    for debtor in report:
        output += f"<p class='mb-3'><strong>Должник - {debtor}:</strong><br>"
        output += "<span class='mt-1'>Требуемые переводы:</span><br>"
        for creditor, charge in report[debtor].items():
            output += f"<span>{creditor} - {charge}</span><br>"
        output += "</p>"
    return output
