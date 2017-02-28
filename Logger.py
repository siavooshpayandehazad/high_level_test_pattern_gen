# Copyright (C) 2015 Siavoosh Payandeh Azad 
import sys
import os
import time


class Logger(object):
    """
    This Class is for redirecting the console messages to a log file...
    """
    def __init__(self):
        if os.path.exists('Console.log'):
            os.remove('Console.log')
        self.terminal = sys.stdout
        self.log = open('Console.log', "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass