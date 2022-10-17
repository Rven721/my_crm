"""Here will be a logic of filterring"""
from cont.models import Contract


def get_contracts_by_agent(contracts, agent_id):
    """will return a list of contracts with agent"""
    return contracts.filter(agent__id=agent_id)


def get_contracts_by_status(contracts, status):
    """will return a list of contracts with given status"""
    return contracts.filter(payment_status=status)


def get_contracts_by_terms_old(contracts, terms_id):
    """will return a list of contracts with given terms"""
    return contracts.filter(terms__id=terms_id)


def create_contract_list_old(request):
    """Will return a list of projects accorging to request attributes"""
    contracts = Contract.objects.all()
    if 'agent' in request.GET:
        contracts = get_contracts_by_agent(contracts, request.GET.get('agent'))
    if 'payment_status' in request.GET:
        contracts = get_contracts_by_status(contracts, request.GET.get('payment_status'))
    if 'terms' in request.GET:
        contracts = get_contracts_by_terms_old(contracts, request.GET.get('terms'))
    return contracts


def parce_contract_search_request(request):
    '''Will parce the request and retur a list of atributes for sarcing'''
    attrs = {
        'number': request.GET['number'],
        'date': request.GET['date'],
        'project': request.GET['project'],
        'agents': [int(agent_id) for agent_id in request.GET.getlist('agent')],
        'terms': [int(terms_id) for terms_id in request.GET.getlist('terms')],
        'payment_statuses': request.GET.getlist('payment_status'),
        'grant_min': request.GET['grant_min'],
        'grant_max': request.GET['grant_max'],
        'project_cost_min': request.GET['project_cost_min'],
        'project_cost_max': request.GET['project_cost_max'],
    }
    for attr, value in attrs.items():
        if len(value) < 1:
            attrs[attr] = None
    return attrs


def check_year(value):
    """Will check given year"""
    return False if int(value) < 4 else True


def check_month(value):
    """Will check given month"""
    return True if int(value) in range(1, 13) else False


def check_day(value):
    """will check date"""
    return True if int(value) in range(1, 32) else False


def check_date(value):
    print(type(value))
    if not any([element in ('1','2', '3', '4', '5', '6', '7', '8', '9', '0', '.') for element in list(value)]):
        return False
    date = value.split('.')
    if len(date) == 1 and check_year(date[0]):
        return True
    if len(date) == 2 and any((check_month(date[0]), check_year(date[1]))):
        return True
    if len(date) == 3 and any((check_day(date[0]), check_month(date[1]), check_year(date[1]))):
        return True
    return False


def get_contracts_by_date(contracts, date):
    """Will return contracts matching given date"""
    if not check_date(date):
        print('bad_date')
        return contracts
    date = date.split('.')
    if len(date) == 1:
        year = date[0]
        return contracts.filter(date__year=year)
    if len(date) == 2:
        month, year = date[0], date[1]
        return contracts.filter(date__month=month, date__year=year)
    if len(date) == 3:
        day, month, year = date[0], date[1], date[2]
        return contracts.filter(date__day=day, date__month=month, date__year=year)


def get_contracts_by_agents(contracts, agents):
    """Will return contracts with given agents"""
    return contracts.filter(agent__id__in=agents)


def get_contracts_by_terms(contracts, terms):
    """Will return contracts with given terms"""
    return contracts.filter(terms__id__in=terms)


def get_contracts_by_payment_statuses(contracts, payment_statuses):
    """Will return contracts with given agents"""
    return contracts.filter(payment_status__in=payment_statuses)


def get_contracts_by_grant_value(contracts, grant_min, grant_max):
    """Will return contracts with given agents"""
    if grant_min:
        contracts = contracts.filter(project__grant__gte=grant_min)
    if grant_max:
        contracts = contracts.filter(project__grant__lte=grant_max)
    return contracts


def get_contracts_by_project_cost(contracts, project_cost_min, project_cost_max):
    """Will return contracts with given agents"""
    if project_cost_min:
        contracts = contracts.filter(project__full_cost__gte=project_cost_min)
    if project_cost_max:
        contracts = contracts.filter(project__full_cost__lte=project_cost_max)
    return contracts


def create_contract_list(request):
    '''Will return a list of project according to request attributes'''
    attrs = parce_contract_search_request(request)
    contracts = Contract.objects.all()
    if attrs['number']:
        contracts = contracts.filter(number=attrs['number'])
    if attrs['date']:
        contracts = get_contracts_by_date(contracts, attrs['date'])
    if attrs['project']:
        contracts = contracts.filter(project__id=attrs['project'])
    if attrs['agents']:
        contracts = get_contracts_by_agents(contracts, attrs['agents'])
    if attrs['terms']:
        contracts = get_contracts_by_terms(contracts, attrs['terms'])
    if attrs['payment_statuses']:
        contracts = get_contracts_by_payment_statuses(contracts, attrs['payment_statuses'])
    if attrs['grant_min'] or attrs['grant_max']:
        contracts = get_contracts_by_grant_value(contracts, attrs['grant_min'], attrs['grant_max'])
    if attrs['project_cost_min'] or attrs['project_cost_max']:
        contracts = get_contracts_by_project_cost(contracts, attrs['project_cost_min'], attrs['project_cost_max'])
    return contracts
