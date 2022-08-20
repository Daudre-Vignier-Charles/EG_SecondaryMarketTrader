#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests

SMSAPI_SENDMSG_URL = 'https://smsapi.free-mobile.fr/sendmsg'
"""URL of the ``sendmsg`` method."""

class MissingParameter(Exception):
    """HTTP error 400: Mandatory parameter is missing."""

class TooManySMS(Exception):
    """HTTP error 402: Too many SMSs have been sent too quickly."""

class ServiceNotEnabled(Exception):
    """HTTP error 403: SMS notification service has not been enabled for this
    user."""

class ServerError(Exception):
    """HTTP error 500: Server error."""

class SMSSender:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
        self.repo = []
    
    def send_contracts(self, contracts):
            self.send_sms(self._format_sms(contracts))
        
    def send_sms(self, message: str) -> None:
        """Sends a message."""
        response = requests.post(
            SMSAPI_SENDMSG_URL,
            json={
                "user": self.username,
                "pass": self.api_key,
                "msg": message
            })
        error = {
            400: MissingParameter,
            402: TooManySMS,
            403: ServiceNotEnabled,
            500: ServerError
        }.get(response.status_code, None)
        if error:
            raise error
        
    def _format_sms(self, contracts): 
        string = "EGS:\r\n"
        for contract in contracts:
            substring = "{ID}# {SELL}e {ROI}% {TIME}d\r\n".format(ID=contract['id'], SELL=contract['sell price'], TIME=contract['remaining time'], ROI=contract['ROI'])
            string += substring
        return string
