import logging

LOG_FILE = 'gameRunner.log'

def logger_config(name):

    logging.basicConfig(filename = LOG_FILE, 
	    format='[%(asctime)s]: [%(filename)s: %(funcName)s: %(lineno)s ] - %(message)s', 
		filemode='w')

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger