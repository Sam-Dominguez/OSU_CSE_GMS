import logging

LOGGER = logging.getLogger('django')

# Disable logging in test cases for clean test results
logging.disable(logging.CRITICAL)