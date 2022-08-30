"""Here forms for CRM live"""

from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import Contact, Company, Project, Status, Event, ProjectDeliver, Task, TaskStatus, RoadMap
from .busines_logic.phone_standartizator import get_standart_phone

BUTTON_BLOCK = Row(
    Column(Submit('submit', 'Сохранить', css_class="btn btn-primary mt-3 fs-5"), css_class="col-auto"),
    Column(HTML("""<a class="btn btn-secondary mt-3 fs-5" href="{{request.META.HTTP_REFERER}}">Выйти без сохранения</a>""")),
    css_class="d-flex flex-row mb-5")


class ContactAddForm(forms.ModelForm):
    """A form for adding a contact"""
    class Meta:
        model = Contact
        fields = ('first_name', 'second_name', 'last_name', 'email', 'phone', 'additional_info')
        widgets = {'additional_info': forms.Textarea(attrs={'rows': 4})}

    def clean_phone(self):
        """will return stardart phone number or raise error"""
        phone = get_standart_phone(self.cleaned_data['phone'])
        if phone == 'bad_number':
            raise forms.ValidationError("Телефон указан не корректно")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='w-30'),
                Column('second_name', css_class='w-30'),
                Column('last_name', css_class='w-30'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
                Column('additional_info', css_class='col-md-6')
            ),
            BUTTON_BLOCK,
        )


class ContactSearchForm(forms.Form):
    """Form for serching a contact"""
    query = forms.CharField(label='Поиск')


class CompanyAddForm(forms.ModelForm):
    """A form for adding a company using DADATA"""
    contacts = forms.ModelMultipleChoiceField(
        Contact.objects.all().order_by("first_name"),
        label="Контакты",
    )

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
    contacts = forms.ModelMultipleChoiceField(
        Contact.objects.all().order_by("first_name"),
        label="Контакты",
    )

    class Meta:
        model = Company
        fields = ('contacts',)


class ProjectAddForm(forms.ModelForm):
    """A form for adding a project"""
    grant = forms.DecimalField(max_digits=11, decimal_places=2, label='Сумма гранта')
    full_cost = forms.DecimalField(max_digits=11, decimal_places=2, label='Бюджет проекта')
    contacts = forms.ModelMultipleChoiceField(
        Contact.objects.all().order_by("first_name"),
        label="Контакты",
        required=False,
    )

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
            'summary',
        )
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'summary': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'full_name',
            Row(
                Column('start_date', css_class='col-md-4 me-3'),
                Column('end_date', css_class='col-md-4 me-3'),
            ),
            Row(
                Column('grant', css_class='w-45'),
                Column('full_cost', css_class='w-45'),
            ),
            Row(
                Column('project_deliver', css_class='w-30'),
                Column('company', css_class='w-30'),
                Column('contacts', css_class='w-30'),
            ),
            Row(
                Column('description', css_class='col-md-6'),
                Column('summary', css_class='col-md-6'),
            ),
            BUTTON_BLOCK,
        )


class ProjectUpdateForm(forms.ModelForm):
    """A form for updating a project details"""
    grant = forms.DecimalField(max_digits=11, decimal_places=2, label='Сумма гранта')
    full_cost = forms.DecimalField(max_digits=11, decimal_places=2, label='Бюджет проекта')
    contacts = forms.ModelMultipleChoiceField(
        Contact.objects.all().order_by("first_name"),
        label="Контакты",
        required=False,
    )

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
            'summary',
        )

        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'summary': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('start_date', css_class='col-md-4 me-3'),
                Column('end_date', css_class='col-md-4 me-3'),
            ),
            Row(
                Column('grant', css_class='w-45'),
                Column('full_cost', css_class='w-45'),
            ),
            Row(
                Column('project_deliver', css_class='w-30'),
                Column('company', css_class='w-30'),
                Column('contacts', css_class='w-30'),
            ),
            Row(
                Column('description', css_class='col-md-6'),
                Column('summary', css_class='col-md-6'),
            ),
            BUTTON_BLOCK,
        )


class ProjectSummaryUpdateForm(forms.ModelForm):
    """A form for updating project_summary"""
    class Meta:
        model = Project
        fields = (
            'summary',
        )


class StatusAddForm(forms.ModelForm):
    """A form for status adding"""
    class Meta:
        model = Status
        fields = ('status',)


class RoadMapForm(forms.ModelForm):
    """A form for to update roadmap of a project"""
    class Meta:
        model = RoadMap
        fields = ('kick_off_meeting', 'contract', 'to_do_list', 'first_pay', 'application')


class EventSmallAddForm(forms.ModelForm):
    """A form for add local event"""

    class Meta:
        model = Event
        fields = ('category', 'description', 'date', 'time', 'took_time', 'result', 'small')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'result': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {'time': 'чч:мм', 'took_time': 'В секундах'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column('category', css_class="col-md-5"),
            Row(
                Column('date', css_class="col-sm-4 col-md-3 me-3"),
                Column('time', css_class="col-sm-3 me-3"),
                Column('took_time', css_class="col-sm-5 col-md-3"),
            ),
            Row(
                Column('description', css_class="col-sm-6"),
                Column('result', css_class="col-sm-6"),
            ),
            'small',
            BUTTON_BLOCK,
        )


class MultipleEventAddForm(forms.ModelForm):
    """A for for adding meeting event"""
    class Meta:
        model = Event
        fields = ('projects', 'category', 'description', 'date', 'time', 'result', 'small')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'result': forms.Textarea(attrs={'rows': 4}),
        }
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
        fields = ('took_time', 'result')


class EventUpdateForm(forms.ModelForm):
    """Form for event update"""
    class Meta:
        model = Event
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'result': forms.Textarea(attrs={'rows': 4}),
            'projects': forms.SelectMultiple(attrs={'size': 1}),
        }
        fields = (
            'projects',
            'category',
            'description',
            'date',
            'time',
            'took_time',
            'result',
            'small',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('category', css_class="col-md-4"),
                Column('projects', css_class="col-md-4"),
            ),
            Row(
                Column('date', css_class="col-sm-4 col-md-3 me-3"),
                Column('time', css_class="col-sm-3 me-3"),
                Column('took_time', css_class="col-sm-5 col-md-3"),
            ),
            Row(
                Column('description', css_class="col-sm-6"),
                Column('result', css_class="col-sm-6"),
            ),
            'small',
            BUTTON_BLOCK,
        )


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


class TaskAddForm(forms.ModelForm):
    """Form for adding a new task"""
    class Meta:
        model = Task
        fields = ('name', 'event', 'start_date', 'end_date', 'doer', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='w-50'),
                Column('event', css_class='w-50'),
            ),
            Row(
                Column('start_date', css_class='w-30'),
                Column('end_date', css_class='w-30'),
                Column('doer', css_class='w-30'),
            ),
            'description',
            BUTTON_BLOCK,
        )


class TaskStatusChangeForm(forms.ModelForm):
    """Form to change a status of a task"""
    class Meta:
        model = TaskStatus
        fields = ('status', )


class DoerChooseForm(forms.ModelForm):
    """Form to choose a doer on a task"""
    class Meta:
        model = Task
        fields = ('doer',)


class EventTaskAddForm(forms.ModelForm):
    """Form for adding a new task for one event"""
    class Meta:
        model = Task
        fields = ('name', 'start_date', 'end_date', 'doer', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            Row(
                Column('start_date', css_class='w-30'),
                Column('end_date', css_class='w-30'),
                Column('doer', css_class='w-30'),
                css_class='justify-content-between',
            ),
            'description',
            BUTTON_BLOCK,
        )
