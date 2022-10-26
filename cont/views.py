"""Views for contracts app"""

from django.shortcuts import render, redirect
from .models import Agent, Terms, Contract
from .forms import AgentForm, TermsForm, ContractForm, ContractReportForm, ContractSearchForm
from .busines_logic import filter_engine


def agent_add_view(request):
    '''Will render a page to create new agent'''
    form = AgentForm()
    if request.method == "POST":
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agents')
    ctx = {'form': form}
    return render(request, 'cont/agent_add.html', ctx)


def agent_details_view(request, agent_id):
    '''Will render a card of one agent'''
    agent = Agent.objects.get(id=agent_id)
    ctx = {
        'agent': agent,
    }
    return render(request, 'cont/agent_card.html', ctx)


def agent_list_view(request):
    '''Will render a list of agents'''
    agents = Agent.objects.all()
    ctx = {
        'agents': agents,
    }
    return render(request, 'cont/agent_list.html', ctx)


def terms_add_view(request):
    '''Will render a page to create new terms'''
    form = TermsForm()
    if request.method == "POST":
        form = TermsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('terms')
    ctx = {'form': form}
    return render(request, 'cont/terms_add.html', ctx)


def terms_details_view(request, terms_id):
    '''Will return a card of one agent'''
    terms = Terms.objects.get(id=terms_id)
    ctx = {
        'terms': terms,
    }
    return render(request, 'cont/terms_card.html', ctx)


def terms_list_view(request):
    '''Will render a list of agents'''
    terms = Terms.objects.all()
    ctx = {
        'terms': terms,
    }
    return render(request, 'cont/terms_list.html', ctx)


def contract_add_view(request):
    '''Will render a page to create new contract'''
    form = ContractForm()
    terms_form = TermsForm()
    if request.method == "POST":
        print(request.POST)
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contracts')
    ctx = {'form': form, 'terms_form': terms_form}
    return render(request, 'cont/contract_add.html', ctx)


def contract_details_view(request, contract_id):
    '''Will render a ccard of one contract'''
    contract = Contract.objects.get(id=contract_id)
    ctx = {
        'contract': contract,
    }
    return render(request, 'cont/contract_card.html', ctx)


def contract_list_view(request):
    '''Will return a list of contracts'''
    contracts = filter_engine.create_contract_list_old(request)
    form = ContractReportForm()
    search_form = ContractSearchForm(request.GET)
    if 'search' in request.GET:
        contracts = filter_engine.create_contract_list(request)
    ctx = {
        'contracts': contracts,
        'form': form,
        'search_form': search_form,
    }
    return render(request, 'cont/contract_list.html', ctx)
