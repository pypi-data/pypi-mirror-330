import logging
import os
import sys
from lpar_activation import activation


def main():
    logging.info("***********BEGIN: main***********")
    if (len(sys.argv) == 2 and os.path.exists(sys.argv[1])):
        logging.info("***********JSON file provided***********")
        logging.info(sys.argv[1])
        activation_obj = activation.Activation(sys.argv[1])
        activation_obj.entry_point()


if __name__ == "__main__":
    main()
