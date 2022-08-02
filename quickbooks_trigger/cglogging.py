# Common logging environment setup
import logging
import os
import sys


class cglogging:

    def __init__(self, level=''):
        self.level = level
        return

    def setup_logging(self):

        try:

            CAG_Logging = os.environ['CAG_Logging']
            CAG_Logging_Boto = os.environ['CAG_Logging_Boto']
            # print('We are in Lambda with CAG logging level= {}'.format(CAG_Logging))
        except:
            CAG_Logging = 'debug'
            CAG_Logging_Boto = 'debug'

        logger = logging.getLogger()

        for h in logger.handlers:
            logger.removeHandler(h)

        h = logging.StreamHandler(sys.stdout)

        # use whatever format you want here
        FORMAT = '%(name)s-%(asctime)s %(message)s'
        h.setFormatter(logging.Formatter(FORMAT))
        logger.addHandler(h)

        if CAG_Logging == 'debug':
            logger.setLevel(logging.DEBUG)
        elif CAG_Logging == 'info':
            logger.setLevel(logging.INFO)
        elif CAG_Logging == 'critical':
            logger.setLevel(logging.CRITICAL)
        elif CAG_Logging == 'error':
            logger.setLevel(logging.ERROR)
        elif CAG_Logging == 'warning':
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.DEBUG)

        if CAG_Logging_Boto == 'debug':
            logging.getLogger('boto3').setLevel(logging.DEBUG)
            logging.getLogger('botocore').setLevel(logging.DEBUG)
            logging.getLogger("urllib3").setLevel(logging.DEBUG)
        elif CAG_Logging_Boto == 'info':
            logging.getLogger('boto3').setLevel(logging.INFO)
            logging.getLogger('botocore').setLevel(logging.INFO)
            logging.getLogger("urllib3").setLevel(logging.INFO)
        elif CAG_Logging_Boto == 'critical':
            logging.getLogger('boto3').setLevel(logging.CRITICAL)
            logging.getLogger('botocore').setLevel(logging.CRITICAL)
            logging.getLogger("urllib3").setLevel(logging.CRITICAL)
        elif CAG_Logging_Boto == 'error':
            logging.getLogger('boto3').setLevel(logging.ERROR)
            logging.getLogger('botocore').setLevel(logging.ERROR)
            logging.getLogger("urllib3").setLevel(logging.ERROR)
        elif CAG_Logging_Boto == 'warning':
            logging.getLogger('boto3').setLevel(logging.WARNING)
            logging.getLogger('botocore').setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)
        else:
            logging.getLogger('boto3').setLevel(logging.DEBUG)
            logging.getLogger('botocore').setLevel(logging.DEBUG)
            logging.getLogger("urllib3").setLevel(logging.DEBUG)

        return logger