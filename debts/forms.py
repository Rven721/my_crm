"""Here will be forms for debts app"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from debts.models import Person, Expense, Transh, Debt

BUTTON_BLOCK = Row(
    Column(Submit('submit', 'Сохранить', css_class="btn btn-primary mt-3 fs-5"), css_class="col-auto"),
    Column(HTML("""<a class="btn btn-secondary mt-3 fs-5" href="{{request.META.HTTP_REFERER}}">Выйти без сохранения</a>""")),
    css_class="d-flex flex-row mb-5")


class PersonForm(forms.ModelForm):
    """Form to add new person"""
    class Meta:
        model = Person
        fields = ('name',)


class ExpenseForm(forms.ModelForm):
    """Form to add new expense"""
    class Meta:
        model = Expense
        fields = ('name', 'comment')


class TranshForm(forms.ModelForm):
    """Form to add new transh"""
    class Meta:
        model = Transh
        fields = ('payer', 'receiver', 'expense', 'date', 'charge', 'return_required')
        widgets = {'date': forms.DateInput(attrs={'class': 'datepicker'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('payer', css_class='w-40'),
                Column('receiver', css_class='w-40'),
            ),
            Row(
                Column('expense', css_class='w-30'),
                Column('date', css_class='w-30'),
                Column('charge', css_class='w-30'),
            ),
            BUTTON_BLOCK,
        )

    def clean_receiver(self):
        """Will rais error if payer and receiver are equall"""
        receiver, payer = self.cleaned_data['receiver'], self.cleaned_data['payer']
        if receiver == payer:
            raise forms.ValidationError("Получатель совпадает с плательщиком")
        return receiver


class DebtForm(forms.ModelForm):
    """Form to add new debt"""
    class Meta:
        models = Debt
        fields = ('creditor', 'debtor', 'charge')
