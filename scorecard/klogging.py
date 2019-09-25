import logging
import datetime

log = logging.getLogger("main")

def template(msg):
    now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S" )
    return "[" + now + "]: " + msg

def error(msg):
    log.error(template(msg))

def info(msg):
    log.info(template(msg))

def warning(msg):
    log.warning(template(msg))

def critical(msg):
    log.critical(template(msg))

def debug(msg):
    log.debug(template(msg))