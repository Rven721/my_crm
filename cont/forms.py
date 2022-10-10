'''Here will be a a list of forms'''
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons, FormActions
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import Agent, Terms, Contract

BUTTON_BLOCK = FormActions(
    Submit('submit', 'Сохранить', css_class="btn btn-primary mt-3 fs-5"),
    HTML("""<a class="btn btn-secondary mt-3 fs-5" href="{{request.META.HTTP_REFERER}}">Выйти без сохранения</a>"""), css_class="d-flex justify-content-start")


class AgentForm(forms.ModelForm):
    '''Form to crate new or update existing agent'''
    class Meta:
        model = Agent
        fields = ('name', 'data')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'data',
            BUTTON_BLOCK,
        )


class TermsForm(forms.ModelForm):
    '''Form alows to crate or update terms records'''
    class Meta:
        model = Terms
        fields = ('name', 'first_pay', 'second_pay', 'success_fee', 'success_fee_base', 'team_fee')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            Row(
                Column('first_pay'),
                Column('second_pay'),
            ),
            Row(
                Column('success_fee'),
                Column('success_fee_base'),
                Column('team_fee'),
            ),
            BUTTON_BLOCK,
        )


class ContractForm(forms.ModelForm):
    '''Form allows to create or update a contract record'''
    class Meta:
        model = Contract
        fields = ('number', 'date', 'project', 'agent', 'terms', 'payment_stauts', 'comment')
        widgets = {'date': forms.DateInput(attrs={'class': 'datepicker'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('number'),
                Column('date'),
            ),
            Row(
                Column('project'),
            ),
            Row(
                Column(
                    FieldWithButtons(
                        'terms',
                        HTML("""<a class="align-self-center ms-2 text-success fs-5" href="{% url 'terms_add' %}"><i class="bi bi-plus-lg"></i></a>"""),
                    ),
                ),
                Column(
                    FieldWithButtons(
                        'agent',
                        HTML("""<a class="align-self-center ms-2 text-success fs-5" href="{% url 'agent_add' %}"><i class="bi bi-plus-lg"></i></a>"""),
                    ),
                ),
            ),
            Row(
                Column('comment'),
            ),
            BUTTON_BLOCK,
        )
