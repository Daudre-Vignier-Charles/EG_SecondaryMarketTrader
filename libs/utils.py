#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import datetime
from importlib import reload
        
class BufferedPrinter():
    def __init__(self):
        self.contracts_header = ""
        self.contracts = []
        self.latest_scraping = ""
        self.notif_SMS = ""
        self.notif_desktop = ""
        self.notif_sound = ""
        self.URL = ""
        self.filters = ""
        
    def clear(self):
        for attr in self.__dict__:
            if type(self.__dict__[attr]) is str:
                setattr(self, attr, "")
            elif type(self.__dict__[attr]) is list:
                setattr(self, attr, [])
        
    def print(self):
        print(self.contracts_header)
        print('\x1b[30m\x1b[47m', end='')
        if type(self.contracts) is list:
            for line in self.contracts:
                print(line)
        else:
            print(self.contracts)
        print('\x1b[39m\x1b[49m', end='')
        print('\n')
        print(self.latest_scraping)
        print()
        print(self.URL)
        print('\n')
        if self.notif_SMS == 'SMS ENABLED':
            csms = "\x1b[32m"
        else:
            csms = "\x1b[31m"
        if self.notif_desktop == 'DESKTOP ENABLED':
            cdesktop = "\x1b[32m"
        else:
            cdesktop = "\x1b[31m"
        if self.notif_sound == 'SOUND ENABLED':
            csound = "\x1b[32m"
        else:
            csound = "\x1b[31m"
        print('{CSMS}{SMS}    {CDESKTOP}{DESKTOP}    {CSOUND}{SOUND}\033[39m\n'.format(CSMS=csms, SMS=self.notif_SMS, CDESKTOP=cdesktop, DESKTOP=self.notif_desktop, CSOUND=csound, SOUND=self.notif_sound))
        print(self.filters)
        
    
def clear_screen():
    print("\x1b[2J\x1b[H")
    
def erase_chars_left(num):
    if type(num) is not int:
        raise TypeError
    print("\x1b[{}D".format(num))

class Notify():
    """Keep trace of notifications configs and update them"""
    def __init__(self, bp):
        self.SMS = False
        self.desktop = False
        self.sound = False
        self.bp = bp
        self.offset = -2
    
    def switch_sms(self):
        if self.SMS:
            self.SMS = False

            self.bp.notif_SMS = 'SMS DISABLED'
        else:
            self.SMS = True
            self.bp.notif_SMS = 'SMS ENABLED'
            
    def switch_desktop(self):
        if self.desktop:
            self.desktop = False
            self.bp.notif_desktop = 'DESKTOP DISABLED'
        else:
            self.desktop = True
            self.bp.notif_desktop = 'DESKTOP ENABLED'
            
    def switch_sound(self):
        if self.sound:
            self.sound = False
            self.bp.notif_sound = 'SOUND DISABLED'
        else:
            self.sound = True
            self.bp.notif_sound = 'SOUND ENABLED'
            
    def status(self):
        if self.SMS:
            self.bp.notif_SMS = 'SMS ENABLED'
        else:
            self.bp.notif_SMS = 'SMS DISABLED'
        if self.desktop:
            self.bp.notif_desktop = 'DESKTOP ENABLED'
        else:
            self.bp.notif_desktop = 'DESKTOP DISABLED'
        if self.sound:
            self.bp.notif_sound = 'SOUND ENABLED'
        else:
            self.bp.notif_sound = 'SOUND DISABLED'

def menu():
    """Print menu"""
    clear_screen()
    print("""x : quitter
r : recharger le fichier de configuration puis scraper
s : scraper maintenant
p : mettre le scraper en pause

n : enable all notification modes
e : enable/disable SMS notifications
d : enable/disable desktop notifications
m : enable/disable sound notifications

Nothing to continue.

""")
    return input(">>> ")

PAUSE_MESSAGE = """##################################
# PAUSE, PRESS ENTER TO CONTINUE #
##################################
"""

def keyboard_interrupt_handler(config_filters, now, bp, sms_sender, notify):
    """Open menu and manage user input and resulting action"""
    try:
        ret = menu()
        if ret == 'x':
            exit()
        elif ret == 'r':
            reload(config_filters)
            clear_screen()
        elif ret == 's':
            clear_screen()
        elif ret == 'e':
            notify.switch_sms()
            continue_wait(bp, now)
        elif ret == 'd':
            notify.switch_desktop()
            continue_wait(bp, now)
        elif ret == 'm':
            notify.switch_sound()
            continue_wait(bp, now)
        elif ret == 'n':
            if not notify.SMS:
                notify.switch_sms()
            if not notify.desktop:
                notify.switch_desktop()
            if not notify.sound:
                notify.switch_sound()
            continue_wait(bp,now)
        elif ret == 'p':
            clear_screen()
            print(PAUSE_MESSAGE)
            input()
            continue_wait(bp, now)
        else:
            continue_wait(bp, now)
        bp.clear()
    except KeyboardInterrupt:
        keyboard_interrupt_handler(config_filters, now, bp, sms_sender, notify)
        
def continue_wait(bp, now):
    clear_screen()
    bp.print()
    tsleep = 15 - (datetime.datetime.now() - now).seconds
    if tsleep > 0:
        time.sleep(tsleep)
    clear_screen()
