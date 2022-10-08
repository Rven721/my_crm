'''Here will be a a list of forms'''
from django import forms
from .models import Agent, Terms, Contract


class AgentForm(forms.ModelForm):
    '''Form to crate new or update existing agent'''
    class Meta:
        model = Agent
        fields = ('name', 'date')


class TermsForm(forms.ModelForm):
    '''Form alows to crate or update terms records'''
    class Meta:
        model = Terms
        fields = ('name', 'first_pay', 'second_pay', 'success_fee', 'success_fee_base', 'team_fee')


class CaotractForm(forms.ModelForm):
    '''Form allows to create or update a contract record'''
    class Meta:
        model = Contract
        fields = ('number', 'date', 'project', 'agent', 'terms', 'payment_stauts', 'comment')
