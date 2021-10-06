from dadata import Dadata
from conf.passes import dadata_token


def get_company_data(ogrn):
    profile = {}
    dadata = Dadata('f609de19b73d432e43f69471386103708a90b903')
    result = dadata.find_by_id('party', ogrn)
    try:
        result = result[0]['data']
    except IndexError:
        profile = None
        return profile
    profile['inn_number'] = str(result['inn'])
    profile['full_name'] = result['name']['full_with_opf']
    profile['short_name'] = result['name']['short_with_opf']
    profile['address'] = result['address']['unrestricted_value']
    return profile
