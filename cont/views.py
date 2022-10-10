"""Views for contracts app"""

from django.shortcuts import render, redirect
from .models import Agent, Terms, Contract
from .forms import AgentForm, TermsForm, ContractForm


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
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contracts')
    ctx = {'form': form}
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
    contracts = Contract.objects.all()
    ctx = {
        'contracts': contracts,
    }
    return render(request, 'cont/contract_list.html', ctx)
