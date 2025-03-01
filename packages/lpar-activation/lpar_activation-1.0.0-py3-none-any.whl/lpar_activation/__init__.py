import logging
from lpar_activation.activation import Activation

# Create and configure logger
logging.basicConfig(filename="log_file.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
