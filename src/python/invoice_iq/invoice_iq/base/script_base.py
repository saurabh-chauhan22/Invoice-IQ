import logging

from logging import INFO

import reloa

class InvoiceBase:
    '''
    Base class for all the invoice iq project
    '''
    def __init__(self, script_name) -> None:
        assert script_name is not None
        self.script_name = script_name
        
    def set_logging_level(self):
        logger = logging.getLogger()
        logger.setLevel(INFO)
    
    def set_logger_handler(self):
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler())
    
    def init_logging(self):
        '''
        Initiate logging framework for the script
        '''
        
        
        logger = logging.basicConfig(filename=self.script_name,)