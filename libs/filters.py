#!/usr/bin/python3
# -*- coding:utf-8 -*-

##### BASE CLASS #####

class _FilterBase():
    filter_string = ''
    string = ''

    
class _Numeric:
    def __init__(self, number):
        if type(number) is not int:
            raise TypeError
        self.string = number

    
##### PRICE #####

class _PriceMin(_FilterBase, _Numeric):
    filter_string = 'filter_inputInvestmentStart'
    
    def __init__(self, number):
        _Numeric.__init__(self, number)


class _PriceMax(_FilterBase, _Numeric):
    filter_string = 'filter_inputInvestmentEnd'
    
    def __init__(self, number):
        _Numeric.__init__(self, number)


##### REMAINING TIME #####

class _RemainingTimeMin(_FilterBase, _Numeric):
    filter_string = 'filter_inputPeriodStart'
    
    def __init__(self, number):
        _Numeric.__init__(self, number)

        
class _RemainingTimeMax(_FilterBase, _Numeric):
    filter_string = 'filter_inputPeriodEnd'
    
    def __init__(self, number):
        _Numeric.__init__(self, number)


##### ROI #####

class _ROIMin(_FilterBase, _Numeric):
    filter_string = 'filter_inputPredictiveStart'
    
    def __init__(self, number):
        _Numeric.__init__(self, number)


class _ROIMax(_FilterBase, _Numeric):
    filter_string = 'filter_inputPredictiveEnd'
    
    def __init__(self, number):
        _Numeric.__init__(self, number)


##### COUNTRY #####

class _CountryBase(_FilterBase, _Numeric):
    filter_string = 'filter_country'
    string = ''


class _Estonia(_CountryBase):
    string = 1


class _Finland(_CountryBase):
    string = 128


class _Germany(_CountryBase):
    string = 131


class _Latvia(_CountryBase):
    string = 138


class _Lithuania(_CountryBase):
    string = 140
    

class _Portugal(_CountryBase):
    string = 150
    

class _Spain(_CountryBase):
    string = 157


class _Sweden(_CountryBase):
    string = 158
    

class _Countries:
    Estonia = _Estonia
    Finland = _Finland
    Germany = _Germany
    Latvia = _Latvia
    Lithuania = _Lithuania
    Portugal = _Portugal
    Spain = _Spain
    Sweden = _Sweden


##### CONTRACT STATE #####

class _ContractStateBase(_FilterBase):
    filter_string = 'filter_currentCashType'


class _Funded(_ContractStateBase):
    string = 'FUNDED'


class _Late(_ContractStateBase):
    string = 'LATE'


class _Defaulted(_ContractStateBase):
    string = 'DEFAULTED'


class _ContractStates:
    Funded = _Funded
    Late = _Late
    Defaulted = _Defaulted

    
##### PAYMENT TYPE #####

class _PaymentTypeBase(_FilterBase):
    filter_string = 'filter_paymentType'


class _Bullet(_PaymentTypeBase):
    string = 'BULLET_COUPONS'


class _FullBullet(_PaymentTypeBase):
    string = 'BULLET_COUPON_ZERO'
    

class _Annuity(_PaymentTypeBase):
    string = 'ANNUITY'
    

class _PaymentTypes:
    Bullet = _Bullet
    FullBullet = _FullBullet
    Annuity = _Annuity
    

##### PROJECT TYPE #####

class _ProjectTypeBase(_FilterBase):
    filter_string = 'filter_projectType'


class _Bridge(_ProjectTypeBase):
    string = 'BRIDGE_LOAN'
    

class _Development(_ProjectTypeBase):
    string = 'BUY'


class _Business(_ProjectTypeBase):
    string = 'DEVELOPMENT_AND_SALE'


class _SaleAdvanced(_ProjectTypeBase):
    string = 'DEVELOPMENT'


class _Refinancing(_ProjectTypeBase):
    string = 'REFINANCING'
    

class _Construction(_ProjectTypeBase):
    string = 'SALES_LEASEBACK'
    

class _Reconstruction(_ProjectTypeBase):
    string = 'MORTGAGE_LOAN'
    

class _ProjectTypes:
    Bridge = _Bridge
    Development = _Development
    Business = _Business
    SaleAdvanced = _SaleAdvanced
    Refinancing = _Refinancing
    Construction = _Construction
    Reconstruction = _Reconstruction
    

##### ALL FILTERS TYPE #####

class Filters:
    PriceMin = _PriceMin
    PriceMax = _PriceMax
    RemainingTimeMin = _RemainingTimeMin
    RemainingTimeMax = _RemainingTimeMax
    ROIMin = _ROIMin
    ROIMax = _ROIMax
    Countries = _Countries
    ContractStates = _ContractStates
    PaymentTypes = _PaymentTypes
    ProjectTypes = _ProjectTypes

    
def _get_URL(filter):
    """return part of request url from a filter"""
    return  "&{}={}".format(filter.filter_string, filter.string)

def get_url(filters):
    """return full request url from a list of filters"""
    url = 'https://estateguru.co/portal/secondaryMarket/ajaxGetLoanList?offset=0&max=100&currentUserId=78860&currentCurrency=&userDetails=&showFutureTransactions=false&order=&sort=&filter_isFilter=true&filterTableId=dataTableMrketList&filter_loanName='
    for filter in filters:
            url += _get_URL(filter)
    return url

def print_filters(bp, config_filters):
    """print filters for debuging or monitoring purpose"""
    string = "Filters :\n"
    for filter in config_filters:
        string += '{:<35}{}\n'.format(filter.filter_string, filter.string)
    bp.filters = string
        
