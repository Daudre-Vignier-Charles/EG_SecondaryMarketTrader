#!/usr/bin/python3
# -*- coding:utf-8 -*-

class Contracts():
    """Represent a set of contracts"""
    CONTRACT_FORMAT_STRING = "{:<50}{:<6}{:<20}{:<11}{:<11}{:<12}{:<12}{:<16}{:<7}{:<12}{}"
    CONTRACT_HEADER = ['name', 'id', 'type', 'country', 'state', 'sell price', 'buy price', 'remaining time', 'ROI', 'date', 'URL']

    def __init__(self):
        self.contracts = []
        
    @staticmethod
    def _pretty_header_formater():
        return Contracts.CONTRACT_FORMAT_STRING.format(*Contracts.CONTRACT_HEADER)

    def _pretty_print_formater(self, contract):
        return Contracts.CONTRACT_FORMAT_STRING.format(*[str(item) for item in list(contract.values())])
        
    def _get_matching(self):
        pass
        
    def pretty_print_contracts(self, bp):
        bp.contracts_header = Contracts._pretty_header_formater()
        table = []
        for contract in self.contracts:
            table.append(self._pretty_print_formater(contract))
        bp.contracts = table
    
    def get_new_contracts(self, contracts):
        new_contracts = [contract for contract in contracts if contract not in self.contracts]
        if new_contracts:
            self.contracts += new_contracts
        return new_contracts
