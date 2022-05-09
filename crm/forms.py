"""Here forms for CRM live"""

from django import forms
from django.utils import timezone
from .models import Contact, Company, Project, Status, Event, ProjectDeliver


class ContactAddForm(forms.ModelForm):
    """A form for adding a contact"""
    class Meta:
        model = Contact
        fields = ('first_name', 'second_name', 'last_name', 'email', 'phone', 'additional_info')


class ContactSearchForm(forms.Form):
    """Form for serching a contact"""
    query = forms.CharField(label='Поиск')


class CompanyAddForm(forms.ModelForm):
    """A form for adding a company using DADATA"""
    class Meta:
        model = Company
        fields = ('ogrn_number', 'contacts')

    def clean_ogrn_number(self):
        """Will return clean ogrn number for company adding"""
        try:
            ogrn_number = int(self.cleaned_data['ogrn_number'])
        except ValueError:
            raise forms.ValidationError('В ОГРН должны быть только цифры')
        if len(str(ogrn_number)) != 13:
            raise forms.ValidationError('Длина ОГРН должна составлять 13 цифр')
        return ogrn_number


class CompanyContactAddForm(forms.ModelForm):
    """A form for adding contact to comapny"""
    class Meta:
        model = Company
        fields = ('contacts',)


class ProjectAddForm(forms.ModelForm):
    """A form for adding a project"""
    grant = forms.DecimalField(max_digits=11, decimal_places=2, label='Сумма гранта')
    full_cost = forms.DecimalField(max_digits=11, decimal_places=2, label='Бюджет проекта')

    class Meta:
        model = Project
        fields = (
            'name',
            'full_name',
            'description',
            'start_date',
            'end_date',
            'grant',
            'full_cost',
            'company',
            'contacts',
            'project_deliver',
        )
        widgets = {
            'full_name': forms.Textarea,
            'start_date': forms.SelectDateWidget,
            'end_date': forms.SelectDateWidget,
        }


class ProjectUpdateForm(forms.ModelForm):
    """A form for updating a project details"""
    grant = forms.DecimalField(max_digits=11, decimal_places=2, label='Сумма гранта')
    full_cost = forms.DecimalField(max_digits=11, decimal_places=2, label='Бюджет проекта')

    class Meta:
        model = Project
        fields = (
            'description',
            'start_date',
            'end_date',
            'grant',
            'full_cost',
            'company',
            'contacts',
            'project_deliver',
        )
        widgets = {
            'start_date': forms.SelectDateWidget,
            'end_date': forms.SelectDateWidget,
        }


class StatusAddForm(forms.ModelForm):
    """A form for status adding"""
    class Meta:
        model = Status
        fields = ('status',)


class EventSmallAddForm(forms.ModelForm):
    """A form for add local event"""
    class Meta:
        model = Event
        fields = ('event_type', 'description', 'date', 'time', 'took_time', 'result', 'small')
        widgets = {'date': forms.SelectDateWidget}
        help_texts = {'time': 'чч:мм'}


class MeetingAddForm(forms.ModelForm):
    """A for for adding meeting event"""
    class Meta:
        model = Event
        fields = ('projects', 'event_type', 'description', 'date', 'time', 'invited_persons', 'small')
        widgets = {'date': forms.SelectDateWidget}
        help_texts = {'time': 'чч:мм'}

    def clean_date(self):
        """Will not alow to add event in the past"""
        date = self.cleaned_data['date']
        if date < timezone.localdate():
            raise forms.ValidationError('Указана дата в прошлом')
        return date


class EventResultAddForm(forms.ModelForm):
    """Form for event results adding"""
    class Meta:
        model = Event
        fields = ('result',)


class EventUpdateForm(forms.ModelForm):
    """Form for event update"""
    class Meta:
        model = Event
        fields = ('projects', 'event_type', 'description', 'date', 'time', 'invited_persons', 'result')


class FilterByCompanyForm(forms.Form):
    """Form for filter by company"""
    company = forms.ModelChoiceField(queryset=Company.objects.all().order_by('short_name'), label='Выберете компанию')


class FilterByCompanyAndSource(forms.Form):
    """Form for filter by company and source"""
    company = forms.ModelChoiceField(
        queryset=Company.objects.all().only('short_name').order_by('short_name'),
        label='Выберете компанию',
        required=False,
    )
    project_deliver = forms.ModelChoiceField(
        queryset=ProjectDeliver.objects.all().only('name').order_by('name'),
        label='Источник проекта',
        required=False,
    )
    project_status = forms.ChoiceField(
        choices=[("", '------')] + Status.status_list,
        label='Текущий статус',
        required=False,
    )
