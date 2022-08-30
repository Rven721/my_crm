from django.db.models import Sum

def get_users(debts):
    """will get users"""
    users = []
    for debt in debts:
        if debt.creditor not in users:
            users.append(debt.creditor)
        if debt.debtor not in users:
            users.append(debt.debtor)
    return users

def get_creditors(debts):
    """Will retur a dict of creditors with total credits for each creditor"""
    users = get_users(debts) 
    creditors = {}
    for user in users:
        total_credit = debts.filter(creditor=user).aggregate(total_credit=Sum('charge'))
        creditors[user.name]=float(total_credit['total_credit']) if total_credit['total_credit'] else 0
    return creditors

def get_debtors(debts):
    """Will return a dict of debtors with total debts for each debtor"""
    users = get_users(debts) 
    debtors = {}
    for user in users:
        total_debt = debts.filter(debtor=user).aggregate(total_debt=Sum('charge'))
        debtors[user.name]=float(total_debt['total_debt']) if total_debt['total_debt'] else 0
    return debtors

def make_debt_calculateon(debts):
    """Will return the list of debts with nettings"""
    creditors = get_creditors(debts)
    debtors = get_debtors(debts)
    results = {'creditors': {}, 'debtors': {}}
    for creditor in creditors:
        result = debtors[creditor] - creditors[creditor]
        if result > 0:
            results['debtors'][creditor] = abs(result)
        else:
            results['creditors'][creditor] = abs(result)
    return results

def get_opt_debts_payers(debts_data):
    """Will return the dict of optimyzed payments"""
    debts = make_debt_calculateon(debts_data)
    result_dict = {debtor: {} for debtor in debts['debtors']}
    while debts['creditors']:
        cur_creditor = max(debts['creditors'])
        cur_credit = debts['creditors'].pop(cur_creditor)
        cur_debtor = max(debts['debtors'])
        cur_debt = debts['debtors'].pop(cur_debtor)
        if cur_credit == cur_debt:
            try:
                result_dict[cur_debtor][cur_creditor] += cur_debt
            except KeyError:
                result_dict[cur_debtor][cur_creditor] = cur_debt
        elif cur_credit > cur_debt:
            try:
                result_dict[cur_debtor][cur_creditor] += cur_debt
            except KeyError:
                result_dict[cur_debtor][cur_creditor] = cur_debt
            debts['creditors'][cur_creditor] = abs(cur_credit - cur_debt)
        else:
            try:
                result_dict[cur_debtor][cur_creditor] += cur_credit
            except KeyError:
                result_dict[cur_debtor][cur_creditor] = cur_credit
            debts['debtors'][cur_debtor] = abs(cur_credit - cur_debt)
    return result_dict

