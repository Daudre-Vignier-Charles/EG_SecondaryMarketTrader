#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import datetime
import threading

import config_filters
from config_logins import logins

import libs.utils as utils
import libs.sms as sms
import libs.scraper as scrap
from libs.filters import get_url, print_filters
from libs.contracts import Contracts
from gi.repository import Notify
from playsound import playsound
import webbrowser

bp = utils.BufferedPrinter()

Notify.init("EGScraper")
notifier = Notify.Notification.new("Matching contract found !")
scraper = scrap.Scraper(logins['ESTATEGURU_LOGIN'], logins['ESTATEGURU_PASSWORD'])
sms_sender = sms.SMSSender(logins['FREEMOBILE_LOGIN'], logins['FREEMOBILE_API_KEY'])
contracts = Contracts()
notify = utils.Notify(bp)

utils.clear_screen()

while True:
    try:
        bp.clear()
        th = threading.Thread(target=playsound, args=['./libs/alarm.mp3'])
        try:
            url = get_url(config_filters.filters)
            new_contracts = contracts.get_new_contracts(scraper.scrap(url))
            contracts.pretty_print_contracts(bp)
            for contract in new_contracts:
                webbrowser.open(contract['url'])
            if notify.SMS:
                sms_sender.send_new_contracts(contracts.contracts)
            if notify.desktop:
                notifier.show()
            if notify.sound:
                th.start()
        except scrap.NoContractFound:
            bp.contracts = "No matching contracts found :( !\nYou can try to put less restrictive criteria."
        except Exception as error:
            print("FATAL ERROR")
            if error.message:
                print(error.message)
            exit()
        now = datetime.datetime.now()
        bp.latest_scraping = "Latest scraping : {}".format(now.strftime("%d.%m.%Y %H:%M:%S"))
        notify.status()
        bp.URL = url
        print_filters(bp, config_filters.filters)
        bp.print()
        time.sleep(15)
        utils.clear_screen()
    except KeyboardInterrupt:
        utils.keyboard_interrupt_handler(config_filters, now, bp, sms_sender, notify)

        
        
