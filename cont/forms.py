'''Here will be a a list of forms'''
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons, FormActions
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Reset
from cont.models import Agent, Terms, Contract
from crm.models import Project

BUTTON_BLOCK = FormActions(
    Submit('submit', 'Сохранить', css_class="btn btn-primary mt-3 fs-5"),
    HTML("""<a class="btn btn-secondary mt-3 fs-5" href="{{request.META.HTTP_REFERER}}">Выйти без сохранения</a>"""), css_class="d-flex justify-content-start")

SEARCH_BUTTON_BLOCK = FormActions(
    Submit('search', 'Подобрать', css_class="btn btn-primary mt-3 fs-5"),
    HTML("""<a class="btn btn-secondary mt-3 fs-5" href="{% url 'contracts' %}">Сбросить</a>"""), css_class="d-flex justify-content-start")

REPORT_BUTTON_BLOCK = FormActions(
    Submit('submit', 'Подобрать', css_class="btn btn-primary mt-3 fs-5"),
    Reset('reset', 'Сбросить', css_class="btn btn-secondary mt-3 fs-5"),
    css_class="d-flex justify-content-start")


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
        fields = ('number', 'date', 'project', 'agent', 'terms', 'payment_status', 'comment')
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
                        HTML("""<a class="align-self-center ms-2 text-success fs-5" href="{% url 'terms_add' %}?from_cont=True"><i class="bi bi-plus-lg"></i></a>"""),
                    ),
                ),
                Column(
                    FieldWithButtons(
                        'agent',
                        HTML("""<a class="align-self-center ms-2 text-success fs-5" href="{% url 'agent_add' %}?from_cont=Ture"><i class="bi bi-plus-lg"></i></a>"""),
                    ),
                ),
            ),
            'payment_status',
            Row(
                Column('comment'),
            ),
            BUTTON_BLOCK,
        )


class ContractSearchForm(forms.Form):
    '''Form for seraching contracts'''
    number = forms.CharField(max_length=15, required=False, label="Номер")
    date = forms.CharField(max_length=10, required=False, label="Дата")
    project = forms.ModelChoiceField(queryset=Project.objects.all(), required=False, label="Проект")
    agent = forms.ModelMultipleChoiceField(
        queryset=Agent.objects.all(),
        required=False,
        label="Агент",
        widget=forms.CheckboxSelectMultiple,
    )
    terms = forms.ModelMultipleChoiceField(
        queryset=Terms.objects.all(),
        required=False,
        label="Триф",
        widget=forms.CheckboxSelectMultiple,
    )
    payment_status = forms.MultipleChoiceField(
        choices=Contract.PAYMENT_STATUS_CHOICES,
        required=False,
        label="Статус",
        widget=forms.CheckboxSelectMultiple,
    )
    grant_min = forms.IntegerField(label="Грант от", required=False)
    grant_max = forms.IntegerField(label="Грант до", required=False)
    project_cost_min = forms.IntegerField(required=False, label="Смета от")
    project_cost_max = forms.IntegerField(required=False, label="Стета до")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.layout = Layout(
            Row(
                Column('number'),
                Column('date'),
            ),
            'project',
            Row(
                Column('agent'),
                Column('terms'),
            ),
            'payment_status',
            Row(
                Column('grant_min'),
                Column('grant_max'),
            ),
            Row(
                Column('project_cost_min'),
                Column('project_cost_max'),
            ),
            SEARCH_BUTTON_BLOCK,
        )


class ContractReportForm(forms.Form):
    '''Will render with fields to add to report'''
    rep_number = forms.BooleanField(required=False, label="Номер")
    rep_date = forms.BooleanField(required=False, label="Дата")
    rep_project = forms.BooleanField(required=False, label="Проект")
    rep_agent = forms.BooleanField(required=False, label="Агент")
    rep_terms = forms.BooleanField(required=False, label="Тариф")
    rep_status = forms.BooleanField(required=False, label="Статус")
    rep_comment = forms.BooleanField(required=False, label="Комментарий")
    rep_fix_1 = forms.BooleanField(required=False, label="Фикс_1")
    rep_fix_2 = forms.BooleanField(required=False, label="Фикс_2")
    rep_fix_total = forms.BooleanField(required=False, label="Фикс_общ")
    rep_success_fee = forms.BooleanField(required=False, label="Плата за успех")
    rep_team_fee = forms.BooleanField(required=False, label="Выручка команды")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.layout = Layout(
            'rep_number',
            'rep_date',
            'rep_project',
            'rep_agent',
            'rep_terms',
            'rep_status',
            'rep_comment',
            'rep_fix_1',
            'rep_fix_2',
            'rep_fix_total',
            'rep_success_fee',
            'rep_team_fee',
            REPORT_BUTTON_BLOCK,
        )
