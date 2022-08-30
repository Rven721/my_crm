"""Here will be veiews for debts app"""
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from debts.models import Person, Expense, Transh, Debt
from debts.forms import PersonForm, ExpenseForm, TranshForm
from debts.busines_logic import transh_proceed as tp
from debts.busines_logic import debt_calc as dc
from debts.busines_logic import report_generator as rg


@login_required
def person_view(request, person_id):
    """Will render a person`s page"""
    person = Person.objects.get(pk=person_id)
    ctx = {'person': person}
    return render(request, 'debts/person_page.html', ctx)


@login_required
def person_add_view(request):
    """Will render a from to add a person"""
    form = PersonForm()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            return redirect('person_page', person.pk)
        return render(request, 'debts/new_person.html', {'form': form})
    return render(request, 'debts/new_person.html', {'form': form})


@login_required
def expense_view(request, expense_id):
    """Will render an expanse page"""
    expense = Expense.objects.get(pk=expense_id)
    ctx = {'expense': expense}
    return render(request, 'debts/expense_page.html', ctx)


@login_required
def expense_add_view(request):
    """Will render a form to add new expense"""
    form = ExpenseForm()
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            return redirect('expense_page', expense.pk)
        return render(request, 'debts/new_expense.html', {'form': form})
    return render(request, 'debts/new_expense.html', {'form': form})


@login_required
def transh_list_view(request, day=None, month=None, year=None):
    """Will render a list of transhes"""
    transh_list = Transh.objects.all().order_by('date').reverse()
    if day and month and year:
        target_date = date(day=day, month=month, year=year)
        transh_list = transh_list.filter(date=target_date)
    return render(request, 'debts/transh_list.html', {'transh_list': transh_list})


@login_required
def transh_view(request, transh_id):
    """Will render a page of a transh"""
    transh = Transh.objects.get(pk=transh_id)
    ctx = {'transh': transh}
    return render(request, 'debts/transh_page.html', ctx)


@login_required
def transh_add_view(request):
    """Will proceed a transh using busines logic"""
    if request.method == "POST":
        form = TranshForm(request.POST)
        if form.is_valid():
            transh = form.save()
            tp.proceed_transh(transh)
            return render(request, 'debts/transh_add_success.html', {'transh_id': transh.id})
        return render(request, 'debts/new_transh.html', {'form': form})
    if request.GET.get('transh_id'):
        template_transh = Transh.objects.get(pk=request.GET['transh_id'])
        form = TranshForm(instance=template_transh)
    else:
        form = TranshForm()
    return render(request, 'debts/new_transh.html', {'form': form})


@login_required
def debt_list_view(request):
    """Will render a lis of all debts"""
    order_by = 'debtor'
    if request.GET.get('order_by'):
        order_by = request.GET['order_by']
    debts = Debt.objects.all().order_by(order_by)
    ctx = {
        'debts': debts,
        'order_by': order_by,
    }
    return render(request, 'debts/debt_list.html', ctx)


@login_required
def debt_calculation_view(request):
    """Will create optimal dept payment order"""
    debts = Debt.objects.all()
    pay_order = dc.get_opt_debts_payers(debts)
    ctx = {'payment_order': rg.form_report(pay_order)}
    return render(request, 'debts/payment_order.html', ctx)


@login_required
def success_page_view(request):
    """Will show success page"""
    return render(request, 'debts/transh_add_success.html', {'transh_id': 40})
