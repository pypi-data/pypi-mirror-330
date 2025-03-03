#!/usr/bin/env python3.11
"""
Provides a common logger for the package, named "logger", and issuing
log messages to the  "goblinfish.pact" log-stream.

Note:
-----
The formatting and outputs of the logger can be modified outside this
module, but that may lead to inconsistent messaging

Environment:
------------
PACT_LOG_LEVEL : (one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    The logging-level to set. If not provided, defaults to "INFO"
LOG_TO_CONSOLE : boolean string (True or False)
    Whether to issue log-messages to the console as well as the normal
    destination or not.
"""

# Built-In Imports
import logging
import os
import sys

# Module "Constants" and Other Attributes
PACT_LOG_LEVELS = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
LOG_FORMAT = '[%(name)s] [%(levelname)s] %(message)s'

# Set up the
if 'logger' not in globals():
    logging.basicConfig(format=LOG_FORMAT, stream=sys.stderr)
    logger = logging.getLogger('goblinfish.pact')
    PACT_LOG_LEVEL = os.getenv('PACT_LOG_LEVEL', 'INFO').upper()
    assert PACT_LOG_LEVEL in PACT_LOG_LEVELS, \
        f'The {PACT_LOG_LEVEL} logging-level is not one of {PACT_LOG_LEVELS}'
    logger.setLevel(PACT_LOG_LEVEL)

assert 'logger' in globals(), \
    f'The logger set-up in {__file__} did not create a logger'

# Code to run if the module is executed directly
if __name__ == '__main__':

    logger.debug('This is a DEBUG log-message')
    logger.info('This is a INFO log-message')
    logger.warning('This is a WARNING log-message')
    logger.error('This is a ERROR log-message')
    logger.critical('This is a CRITICAL log-message')
